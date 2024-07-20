# Telegram Piggy Bank Bot

This is a Telegram bot that helps users save money, track their expenses, and manage their finances in a fun and engaging way.

## Features

- User Registration and Authentication
- Balance Tracking
- Deposit and Withdrawal Functions
- Savings Goals
- Expense Tracking
- Notifications and Reminders
- Security

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/your_username/telegram-piggy-bank-bot.git
   cd telegram-piggy-bank-bot
   ```

2. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Add your Telegram bot token and Firebase credentials:

   - Create a `.env` file and add your Telegram bot token:

     ```plaintext
     TELEGRAM_BOT_TOKEN=your_bot_token
     ```

   - Replace `"path/to/your/firebase_credentials.json"` in `bot.py` with the actual path to your Firebase credentials JSON file.

4. Run the bot:

   ```sh
   python bot.py
   ```

## Usage

- `/start` - Register or authenticate the user.
- `/balance` - Show the current balance.
- `/deposit <amount>` - Deposit money into the piggy bank.
- `/withdraw <amount>` - Withdraw money from the piggy bank.
- `/setgoal <goal>` - Set a savings goal.
- `/viewgoals` - View current savings goals.
- `/addexpense <category> <amount>` - Add an expense.
- `/viewexpenses` - View recorded expenses.

## License

This project is licensed under the MIT License.
