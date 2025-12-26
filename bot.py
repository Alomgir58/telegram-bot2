import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Railway Variables থেকে Token নেবে
8234194379:AAGlt-BzhP7EmJTNmMvAI27AcCK5Ncb0wfU = os.getenv("8234194379:AAGlt-BzhP7EmJTNmMvAI27AcCK5Ncb0wfU")

# তোমার নিজের রিপোর্ট URL
REPORT_URL = "http://94.23.120.156/ints/agent/SMSCDRStats"

def get_sms_report():
    response = requests.get(REPORT_URL, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # পুরো পেজ থেকে টেক্সট নেবে
    text = soup.get_text(separator="\n")

    # ফাঁকা লাইন বাদ
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # Telegram message ছোট রাখতে
    report = "\n".join(lines[:25])

    return report


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 SMS CDR Report Bot\n\n"
        "রিপোর্ট দেখতে 👉 /report লিখুন"
    )


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = get_sms_report()
        await update.message.reply_text(
            f"📈 Latest SMS Report:\n\n{data}"
        )
    except Exception:
        await update.message.reply_text(
            "❌ রিপোর্ট আনতে সমস্যা হয়েছে"
        )


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("report", report))

print("Bot is running...")
app.run_polling()
