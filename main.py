import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# ================================
# LOGGING
# ================================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # isi ADMIN_ID di Railway (opsional)

# ================================
# COMMAND: /start
# ================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Cek Status Bot", callback_data="status")],
        [InlineKeyboardButton("Menu Lainnya", callback_data="menu_lain")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Halo! 👋\nBot Telegram sudah online!\nSilakan pilih menu:",
        reply_markup=reply_markup
    )

# ================================
# COMMAND: /hello
# ================================
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo juga! 😄")

# ================================
# COMMAND: /say <text>
# ================================
async def say(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        return await update.message.reply_text("Contoh penggunaan:\n/say Halo semuanya!")

    text = " ".join(context.args)
    await update.message.reply_text(f"Kamu bilang: {text}")

# ================================
# COMMAND: /admin (hanya untuk admin)
# ================================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        return await update.message.reply_text("❌ Kamu bukan admin.")

    await update.message.reply_text("Halo admin! Semua aman.")

# ================================
# CALLBACK BUTTON HANDLER
# ================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "status":
        await query.edit_message_text("Bot sedang **online & berjalan normal** ✔️")
    
    elif data == "menu_lain":
        await query.edit_message_text(
            "Menu lainnya:\n- /hello\n- /say <text>\n- /admin (khusus admin)"
        )

# ================================
# ERROR HANDLER
# ================================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Error terjadi:", exc_info=context.error)

    try:
        if update and update.effective_message:
            await update.effective_message.reply_text("⚠️ Terjadi error, coba lagi nanti.")
    except:
        pass

# ================================
# MAIN APP
# ================================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Daftar command handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("say", say))
    app.add_handler(CommandHandler("admin", admin))

    # Inline button callback
    app.add_handler(CallbackQueryHandler(button_handler))

    # Error handler
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
