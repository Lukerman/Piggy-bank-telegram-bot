import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase
cred = credentials.Certificate("path/to/your/firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Telegram Bot
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

# Scheduler for notifications
scheduler = BackgroundScheduler()
scheduler.start()

# User Registration and Authentication
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_data = db.collection('users').document(str(user_id)).get().to_dict()
    if not user_data:
        db.collection('users').document(str(user_id)).set({'balance': 0.0, 'goals': [], 'expenses': []})
        bot.reply_to(message, f'Welcome {message.from_user.first_name}! Your account has been created.')
    else:
        bot.reply_to(message, f'Welcome back {message.from_user.first_name}!')

# Balance Tracking
@bot.message_handler(commands=['balance'])
def balance(message):
    user_id = message.from_user.id
    user_data = db.collection('users').document(str(user_id)).get().to_dict()
    balance = user_data.get('balance', 0.0)
    bot.reply_to(message, f'Your current balance is ${balance:.2f}.')

# Deposit Function
@bot.message_handler(commands=['deposit'])
def deposit(message):
    try:
        amount = float(message.text.split()[1])
        user_id = message.from_user.id
        user_ref = db.collection('users').document(str(user_id))
        user_data = user_ref.get().to_dict()
        new_balance = user_data['balance'] + amount
        user_ref.update({'balance': new_balance})
        bot.reply_to(message, f'Deposited ${amount:.2f}. New balance is ${new_balance:.2f}.')
    except (IndexError, ValueError):
        bot.reply_to(message, 'Please provide a valid amount. Usage: /deposit <amount>')

# Withdrawal Function
@bot.message_handler(commands=['withdraw'])
def withdraw(message):
    try:
        amount = float(message.text.split()[1])
        user_id = message.from_user.id
        user_ref = db.collection('users').document(str(user_id))
        user_data = user_ref.get().to_dict()
        new_balance = user_data['balance'] - amount
        if new_balance < 0:
            bot.reply_to(message, 'Insufficient balance.')
        else:
            user_ref.update({'balance': new_balance})
            bot.reply_to(message, f'Withdrew ${amount:.2f}. New balance is ${new_balance:.2f}.')
    except (IndexError, ValueError):
        bot.reply_to(message, 'Please provide a valid amount. Usage: /withdraw <amount>')

# Set Savings Goals
@bot.message_handler(commands=['setgoal'])
def set_goal(message):
    try:
        goal = message.text.split(maxsplit=1)[1]
        user_id = message.from_user.id
        user_ref = db.collection('users').document(str(user_id))
        user_data = user_ref.get().to_dict()
        goals = user_data.get('goals', [])
        goals.append(goal)
        user_ref.update({'goals': goals})
        bot.reply_to(message, f'Savings goal "{goal}" set!')
    except IndexError:
        bot.reply_to(message, 'Please provide a valid goal. Usage: /setgoal <goal>')

# View Savings Goals
@bot.message_handler(commands=['viewgoals'])
def view_goals(message):
    user_id = message.from_user.id
    user_data = db.collection('users').document(str(user_id)).get().to_dict()
    goals = user_data.get('goals', [])
    goals_text = '\n'.join(goals) if goals else 'No goals set.'
    bot.reply_to(message, f'Your savings goals:\n{goals_text}')

# Add Expense
@bot.message_handler(commands=['addexpense'])
def add_expense(message):
    try:
        args = message.text.split(maxsplit=2)
        category, amount = args[1], float(args[2])
        expense = {'category': category, 'amount': amount}
        user_id = message.from_user.id
        user_ref = db.collection('users').document(str(user_id))
        user_data = user_ref.get().to_dict()
        expenses = user_data.get('expenses', [])
        expenses.append(expense)
        user_ref.update({'expenses': expenses})
        bot.reply_to(message, f'Expense of ${amount:.2f} in category "{category}" added!')
    except (IndexError, ValueError):
        bot.reply_to(message, 'Please provide valid details. Usage: /addexpense <category> <amount>')

# View Expenses
@bot.message_handler(commands=['viewexpenses'])
def view_expenses(message):
    user_id = message.from_user.id
    user_data = db.collection('users').document(str(user_id)).get().to_dict()
    expenses = user_data.get('expenses', [])
    expenses_text = '\n'.join([f"{e['category']}: ${e['amount']:.2f}" for e in expenses]) if expenses else 'No expenses recorded.'
    bot.reply_to(message, f'Your expenses:\n{expenses_text}')

# Set up a daily reminder (example)
def send_reminder():
    users = db.collection('users').stream()
    for user in users:
        user_id = user.id
        bot.send_message(user_id, "Don't forget to save today!")

# Schedule daily reminders at a specific time
scheduler.add_job(send_reminder, 'interval', days=1, start_date=datetime.now() + timedelta(seconds=10))

# Start the bot
bot.polling()
