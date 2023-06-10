from flask import Flask, request
import os
import telebot

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('mega_bot'), threaded=False)
bot.set_webhook(url = os.getenv('url'))

# Bot route to handle incoming messages
@app.route('/', methods=['POST'])
def telegram():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200

# Command: /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    send_log(bot, message)
    # Handle the /start command
    name =  message.from_user.username or message.from_user.first_name or message.from_user.last_name
    bot.reply_to(message, f"Hello {name}! If you want to see the available commands, type /help.")
