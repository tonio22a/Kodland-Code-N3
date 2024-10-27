#!/usr/bin/python

# This is a simple bot with schedule timer
# https://schedule.readthedocs.io

import time, threading, schedule
import telebot

API_TOKEN = '7876584346:AAHId83U9P5u0faYAsZEmjOu_5wnWldh74c'
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! используй /set (sec) для того, чтобы поставить таймер")


def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Туту!')


@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Используй: /set <sec>')


@bot.message_handler(commands=['ping'])
def poping(message):
    bot.reply_to(message, 'Pong!')

@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
