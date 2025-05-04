import time
import threading
import schedule
from flask import Flask
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

# Flask app to keep Render service alive
app = Flask(__name__)

# Your Telegram Bot token from @BotFather
BOT_TOKEN = 'YOUR_BOT_TOKEN'
bot = Bot(token=BOT_TOKEN)

# Global variable to store group chat ID (update after you get it)
GROUP_CHAT_ID = -1001234567890  # Replace this after Step 1 is done

# ✅ Step 1: Function to print chat ID (used once to get your group chat ID)
def handle_all_messages(update: Update, context: CallbackContext):
    chat = update.effective_chat
    print(f"Chat ID: {chat.id}")
    if chat.type in ['group', 'supergroup']:
        context.bot.send_message(chat_id=chat.id, text=f"✅ This group's chat ID is: {chat.id}")

# ✅ Step 2: Scheduled message functions
def send_morning():
    bot.send_message(chat_id=GROUP_CHAT_ID, text="🌞 Good morning, everyone!")

def send_lunch():
    bot.send_message(chat_id=GROUP_CHAT_ID, text="🍱 Don't forget to take a lunch break!")

def send_evening():
    bot.send_message(chat_id=GROUP_CHAT_ID, text="🌙 Good evening! Wind down and relax.")

# ✅ Step 3: Background scheduler thread
def run_scheduler():
    schedule.every().day.at("08:00").do(send_morning)
    schedule.every().day.at("13:00").do(send_lunch)
    schedule.every().day.at("19:00").do(send_evening)

    while True:
        schedule.run_pending()
        time.sleep(1)

# ✅ Flask endpoint to keep app alive
@app.route('/')
def home():
    return "Telegram bot is running."

# ✅ Start everything (Flask + Telegram Dispatcher + Scheduler)
if __name__ == '__main__':
    from telegram.ext import Updater
    updater = Updater(BOT_TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.all, handle_all_messages))  # Used to get group chat ID

    threading.Thread(target=run_scheduler).start()
    updater.start_polling()
    app.run(host='0.0.0.0', port=8080)
