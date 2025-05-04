import os
import time
import datetime
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import schedule
import threading
from flask import Flask
from dotenv import load_dotenv  # This is useful if you use .env locally, but not needed on Replit

# --- Load environment variables ---
# On Replit, no need for dotenv as Replit manages this directly
BOT_TOKEN = os.getenv(
    "BOT_TOKEN")  # Securely get the token from the environment variable
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# --- Debugging: Check if the environment variables are loaded correctly ---
if not BOT_TOKEN or not GROUP_CHAT_ID:
    print(
        "Error: BOT_TOKEN or GROUP_CHAT_ID is missing from environment variables."
    )
else:
    print(f"Bot Token: {BOT_TOKEN}")
    print(f"Group Chat ID: {GROUP_CHAT_ID}")

# Flask app to keep the bot alive
app = Flask(__name__)


@app.route('/')
def home():
    return 'Bot is running!'


# Start command (optional)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, I'm alive and working!")


# --- Send message to Telegram group ---
def send_scheduled_message(message):

    async def send():
        try:
            application = ApplicationBuilder().token(BOT_TOKEN).build()
            await application.bot.send_message(chat_id=GROUP_CHAT_ID,
                                               text=message)
            print(
                f"[{datetime.datetime.now()}] Message sent successfully: {message}"
            )
        except Exception as e:
            print(f"Error sending message: {e}")

    asyncio.run(send())


# --- Scheduled task setup ---
def job():
    print("Setting up scheduled messages...")

    # ✅ Set test time close to now for testing
    schedule.every().day.at("16:45").do(lambda: send_scheduled_message(
        "🧪 Scheduled test message sent successfully!"))

    # Daily messages
    schedule.every().day.at("08:00").do(
        lambda: send_scheduled_message("🌞 Good Morning!Gundaaaaaa"))
    schedule.every().day.at("13:30").do(
        lambda: send_scheduled_message("🍽️ Good Afternoon!Sapteyaaa"))
    schedule.every().day.at("18:00").do(
        lambda: send_scheduled_message("🌇 Good Evening!Drink water"))
    schedule.every().day.at("22:30").do(
        lambda: send_scheduled_message("🌙Sleeping time Good Night! Gundaaaaa"))

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        print(f"[{current_time}] Scheduled jobs are running...")
        schedule.run_pending()
        time.sleep(10)


# --- Run scheduler in a background thread ---
def run_schedule():
    thread = threading.Thread(target=job)
    thread.daemon = True
    thread.start()


# --- Main execution ---
if __name__ == "__main__":
    print("Starting bot...")
    print("Current server time:",
          datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    run_schedule()

    # ✅ Immediate test message

    # Keep Replit project alive
    app.run(host="0.0.0.0", port=8080)
