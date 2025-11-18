import os
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
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

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ini adalah test command"
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Tombol 1", callback_data="btn1"),
            InlineKeyboardButton("Tombol 2", callback_data="btn2")
        ],
        [
            InlineKeyboardButton("Google", url="https://google.com")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Silakan pilih tombol di bawah:",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "btn1":
        await query.edit_message_text("Kamu menekan *Tombol 1* 👍", parse_mode="Markdown")
    elif query.data == "btn2":
        await query.edit_message_text("Ini *Tombol 2* 👌", parse_mode="Markdown")



# ==========================
#  MAIN APP
# ==========================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # daftar command
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("test", menu))
    app.add_handler(CallbackQueryHandler(button_handler))


    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
