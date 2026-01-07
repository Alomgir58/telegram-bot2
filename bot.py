import os
import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

BOT_TOKEN = os.getenv("8234194379:AAGlt-BzhP7EmJTNmMvAI27AcCK5Ncb0wfU")
REPORT_URL = "http://94.23.120.156/ints/agent/SMSCDRStats"

def get_sms_report():
    response = requests.get(REPORT_URL, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator="\n")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    report = "\n".join(lines[:25])
    return report

# Start command with inline button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📈 Show Report", callback_data="report")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

# Callback for button clicks
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "report":
        try:
            data = get_sms_report()
            await query.edit_message_text(f"📊 Latest SMS Report:\n\n{data}")
        except Exception:
            await query.edit_message_text("❌ Could not fetch report")
    elif query.data == "help":
        await query.edit_message_text("Use the 📈 Show Report button to see the latest SMS report")

# Telegram bot setup
app = ApplicationBuilder().token(8234194379:AAGlt-BzhP7EmJTNmMvAI27AcCK5Ncb0wfU).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))

print("Bot is running...")
app.run_polling()

