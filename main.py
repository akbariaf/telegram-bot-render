import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler
)

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# ============================
# /start
# ============================
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Cek Status Bot", callback_data="status")],
        [InlineKeyboardButton("Menu Lainnya", callback_data="menu_lain")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Halo! 👋\nBot Telegram sudah online!\nSilakan pilih menu:",
        reply_markup=reply_markup
    )

# ============================
# /hello
# ============================
def hello(update, context):
    update.message.reply_text("Halo juga! 😄")

# ============================
# /say <text>
# ============================
def say(update, context):
    if len(context.args) == 0:
        update.message.reply_text("Contoh:\n/say Halo bot!")
        return
    
    text = " ".join(context.args)
    update.message.reply_text(f"Kamu bilang: {text}")

# ============================
# /admin (khusus admin)
# ============================
def admin(update, context):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("❌ Kamu bukan admin.")
        return
    
    update.message.reply_text("Halo admin! 😊")

# ============================
# Button handler
# ============================
def button_handler(update, context):
    query = update.callback_query
    data = query.data

    if data == "status":
        query.edit_message_text("Bot online ✔️")
    elif data == "menu_lain":
        query.edit_message_text(
            "Menu lainnya:\n- /hello\n- /say <text>\n- /admin (khusus admin)"
        )

# ============================
# Main
# ============================
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hello", hello))
    dp.add_handler(CommandHandler("say", say))
    dp.add_handler(CommandHandler("admin", admin))

    # Button handler
    dp.add_handler(CallbackQueryHandler(button_handler))

    # Mulai polling
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
