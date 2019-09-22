from telegram.ext import Updater, CommandHandler
from random import randint
import importlib
import datetime
import yaml
import os
import re
import logging
import daemon
import requests

'''
proxy = 'https://54.39.53.104:3128'
os.environ['HTTP_PROXY'] = proxy
os.environ['HTTPS_PROXY'] = proxy
'''

class Globals:
    def __init__(self, updater, dp, config):
        self.updater = updater
        self.dp = dp
        self.config = config


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',	
                    level=logging.INFO)	
logger = logging.getLogger(__name__)	
logging.getLogger("telegram.utils.promise").propagate = False

with open("resources/logo.txt", "r", encoding="UTF-8") as logo_file:
    logo = logo_file.read()
    print(logo)

with open("config.example.yml", "r") as f:
    config = yaml.load(f)
key = config["keys"]["telegram_token"]
updater = Updater(token=key)
dp = updater.dispatcher
bot_id = requests.get('https://api.telegram.org/bot{}/getMe'.format(key)).json()['result']['id']



for feature in config["features"]:
    if "path" in config["features"][feature]:
        path = config["features"][feature]["path"]
        if not os.path.exists(path):
            os.makedirs(path)
    if config["features"][feature]["enabled"] is True:
        module_config = config["features"][feature]
        module_config['bot_id'] = bot_id
        global_data = gd = Globals(updater, dp, module_config)
        module = importlib.import_module("modules." + feature).module_init(gd)
        print(feature)

# Import /help from a text file
with open("resources/help.txt", "r", encoding="UTF-8") as helpfile:
    help_text = helpfile.read()
    print("Help textfile imported")


# Start feature
def start(bot, update):
    if update.message.chat.type != "private":
        return
    with open("resources/hello.webp", "rb") as hello:
        update.message.reply_sticker(hello, quote=False)
    personname = update.message.from_user.first_name
    update.message.reply_text("Konnichiwa, " + personname + "! \nMy name is Takanashi Rikka desu! \
                              \nUse /help to see what I can do! :3", quote=False)
    print(datetime.datetime.now(), ">>>", "Done /start", ">>>", update.message.from_user.username)
dp.add_handler(CommandHandler("start", start))


# Show help
def help(bot, update):
    bot.send_message(update.message.chat_id, help_text, parse_mode="Markdown")
    print(datetime.datetime.now(), ">>>", "Done /help", ">>>", update.message.from_user.username)
dp.add_handler(CommandHandler("help", help))


# Starting bot
port = os.environ.get('PORT', 5000)
updater.start_webhook(clean=True, bootstrap_retries=0, port=port, url_path=key)
print("=====================\nUp and running!\n")
# Idle
updater.idle()
