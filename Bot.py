import os
from telegram.ext import Updater, MessageHandler, Filters

TOKEN = os.environ.get("TOKEN")  # Ambil token dari Render

def handler(update, context):
    text = update.message.text.lower()

    if text == "halo":
        update.message.reply_text("Hai juga dari bot Python Render!")
    else:
        update.message.reply_text("Bot ini berjalan 24 jam di Render!")

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text, handler))

updater.start_polling()
updater.idle()
