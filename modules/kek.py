#!/usr/bin/python
# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler, MessageHandler
from modules.custom_filters import caption_filter
from modules.send_image import send_image
from modules.get_image import get_image
from telegram import ChatAction
import subprocess
import datetime
import yaml


def handler(dp):
    dp.add_handler(MessageHandler(caption_filter("/kek"), kek))
    dp.add_handler(CommandHandler("kek", kek))

# import path
with open("config.yml", "r") as f:
    path = yaml.load(f)["path"]["kek"]


# get image, pass parameter
def kek(bot, update):
    if update.message.reply_to_message is not None:
        kek_param = "".join(update.message.text[5:7])
    else:
        kek_param = "".join(update.message.caption[5:7])
    try:
        extension = get_image(bot, update, path)
    except:
        update.message.reply_text("Can't get the image! :(")
        return
    update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)
    result = kekify(bot, update, kek_param, extension)
    send_image(bot, update, path, result, extension)
    print(datetime.datetime.now(), ">>>", "Done kek", ">>>", update.message.from_user.username)


# kek process + send
def kekify(bot, update, kek_param, extension):
    try:
        if kek_param == "-l" or kek_param == "":
            crop = "50%x100% "
            piece_one = "result-0" + extension
            piece_two = "result-1" + extension
            flip = "-flop "
            order = path + piece_one + " " + path + piece_two
            append = "+append "
            result = "kek-left"
        elif kek_param == "-r":
            crop = "50%x100% "
            piece_one = "result-1" + extension
            piece_two = "result-0" + extension
            flip = "-flop "
            order = path + piece_two + " " + path + piece_one
            append = "+append "
            result = "kek-right"
        elif kek_param == "-t":
            crop = "100%x50% "
            piece_one = "result-0" + extension
            piece_two = "result-1" + extension
            flip = "-flip "
            order = path + piece_one + " " + path + piece_two
            append = "-append "
            result = "kek-top"
        elif kek_param == "-b":
            crop = "100%x50% "
            piece_one = "result-1" + extension
            piece_two = "result-0" + extension
            flip = "-flip "
            order = path + piece_two + " " + path + piece_one
            append = "-append "
            result = "kek-bot"
        elif kek_param == "-m":
            kekify(bot, update, "-l", extension)
            kekify(bot, update, "-r", extension)
            kekify(bot, update, "-t", extension)
            kekify(bot, update, "-b", extension)
            append_lr = "convert " + path + "kek-left" + extension + " " + path + "kek-right" + extension + " +append " + path + "kek-lr-temp" + extension
            subprocess.run(append_lr, shell=True)
            append_tb = "convert " + path + "kek-top" + extension + " " + path + "kek-bot" + extension + " +append " + path + "kek-tb-temp" + extension
            subprocess.run(append_tb, shell=True)
            append_all = "convert " + path + "kek-lr-temp" + extension + " " + path + "kek-tb-temp" + extension + " -append " + path + "multikek" + extension
            subprocess.run(append_all, shell=True)
            result = "multikek"
            return result
        cut = "convert " + path + "original" + extension + " -crop " + crop + path + "result" + extension
        subprocess.run(cut, shell=True)
        mirror = "convert " + path + piece_one + " " + flip + " " + path + piece_two
        subprocess.run(mirror, shell=True)
        append = "convert " + order + " " + append + path + result + extension
        subprocess.run(append, shell=True)
        return result
    except:
        update.message.reply_text("Unknown kek parameter.\nUse -l, -r, -t, -b or -m")
