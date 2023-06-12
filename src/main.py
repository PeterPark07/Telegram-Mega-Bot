from flask import Flask, request
import time
import os
import telebot
from helper.mega_acc import m

app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('mega_bot'), threaded=False)
download_path = './mega'  # Specify the download directory
# Create the download directory if it doesn't exist
os.makedirs(download_path, exist_ok=True)

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
    # Handle the /start command
    name =  message.from_user.username or message.from_user.first_name or message.from_user.last_name
    bot.reply_to(message, f"Hello {name}! If you want to see the available commands, type /help.\nYour email is {m.get_user()['email']}")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    link = message.text
    try:
        bot.reply_to(message, "Downloading...")
        
        request = m.get_public_url_info(link)
        file_size_int = int(request['size']) / (1024 * 1024)
        file_size = f"{file_size_int} MBs"
        file_name = request['name']
        
        bot.reply_to(message, f"Download info:\n{file_name}\nSize : {file_size}")
        os.chdir(download_path)
        start_time = time.time()  # Capture start time

        file = m.download_url(link)
        os.chdir('..')

        end_time = time.time()  # Capture end time
        download_time = round(end_time - start_time, 2)  # Calculate download time
        download_speed = round(file_size_int / download_time, 2)  # Calculate download speed in MB/s

        bot.reply_to(message, f"File Downloaded.\nTime taken : {download_time} seconds.\nDownload speed: {download_speed} MB/s.\n")
    except Exception as e:
        bot.reply_to(message, f"Could not download: {e}")