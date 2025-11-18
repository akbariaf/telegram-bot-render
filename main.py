import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

# ==========================
#  COMMAND HANDLERS
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Telegram sudah online dengan PTB v20!")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Halo {update.effective_user.first_name} 👋")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ini adalah bot dengan python-telegram-bot versi 20.x"
    )

# ==========================
#  MAIN APP
# ==========================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # daftar command
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("info", info))

    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
