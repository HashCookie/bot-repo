from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

app = Flask(__name__)

TOKEN = os.environ.get('BOT_TOKEN')
bot = telegram.Bot(token=TOKEN)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your Telegram bot.")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    
    dp = Updater(TOKEN, use_context=True).dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    dp.process_update(update)
    return 'ok'

@app.route('/')
def index():
    return 'Bot is running'

if __name__ == '__main__':
    app.run()