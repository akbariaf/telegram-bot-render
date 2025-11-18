import os
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")
ASK_NAME, ASK_AGE, CONFIRM = range(3)
user_cache = {}


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

async def cek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ini adalah test command"
    )

async def start_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_cache[user_id] = {}   # buat memory untuk user ini

    await update.message.reply_text("Silakan masukkan nama Anda:")
    return ASK_NAME
    
async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_cache[user_id]["name"] = update.message.text

    await update.message.reply_text("Berapa umur Anda?")
    return ASK_AGE


async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_cache[user_id]["age"] = update.message.text

    name = user_cache[user_id]["name"]
    age = user_cache[user_id]["age"]

    await update.message.reply_text(
        f"Periksa kembali data Anda:\n\n"
        f"Nama : {name}\n"
        f"Umur : {age}\n\n"
        f"Ketik **yes** untuk simpan, **no** untuk batalkan."
    )

    return CONFIRM


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()

    if text == "yes":
        data = user_cache[user_id]
        await update.message.reply_text("Data berhasil disimpan sementara di cache! 🙌")
        print("Data user:", data)  # contoh penyimpanan
    else:
        await update.message.reply_text("Form dibatalkan.")

    user_cache.pop(user_id, None)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_cache.pop(user_id, None)

    await update.message.reply_text("Form dibatalkan.")
    return ConversationHandler.END

form_handler = ConversationHandler(
    entry_points=[CommandHandler("form", start_form)],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
        ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
        CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
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
    app.add_handler(CommandHandler("cek", cek))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(form_handler)


    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
