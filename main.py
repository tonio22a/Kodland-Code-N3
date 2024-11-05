import time
import threading
import schedule
import telebot
import os
import random

API_TOKEN = 'не покажу токен'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Используйте /help для того, чтобы прочитать список команд.")

def beep(chat_id) -> None:
    """Таймер"""
    try:
        bot.send_message(chat_id, text='Таймер!')
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

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
    start_time = time.monotonic()
    reply_message = bot.reply_to(message, 'Мы анализируем ваш ping.')
    ping = (time.monotonic() - start_time) * 1000
    bot.edit_message_text(chat_id=message.chat.id, message_id=reply_message.message_id, text=f'Ваш пинг: {int(ping)}ms. Pong!')

@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)
    bot.reply_to(message, "Таймер успешно остановлен и выключен.")

@bot.message_handler(commands=['mem'])
def send_mem(message):
    path = os.path.abspath('images')  # абсолютный путь к папке с изображениями
    meme_list = os.listdir(path)  # список всех изображений в папке

    if len(meme_list) < 3:  # проверка, что хотя бы 3 изображения
        bot.reply_to(message, "У нас должно быть хотя бы три изображения в папке.")
        return

    weights = [0, 3, 5, 2]

    if len(weights) != len(meme_list):
        bot.reply_to(message, "Количество весов не соответствует количеству изображений.")
        return

    chosen_image = random.choices(meme_list, weights=weights)[0]

    meme_path = os.path.join(path, chosen_image)  # абсолютный путь к выбранному изображению
    with open(meme_path, 'rb') as f:  # открываем файл
        bot.send_photo(message.chat.id, f)  # отправляем файл

@bot.message_handler(commands=['animals'])
def send_animals_mem(message):
    animpath = os.path.abspath('images/anima')  # абсолютный путь к папке с изображениями
    animmeme_list = os.listdir(animpath)  # список изображений

    if len(animmeme_list) < 3:
        bot.reply_to(message, "У нас должно быть хотя бы три изображения в папке.")
        return

    weights = [5, 2, 3]

    animrandom_meme = random.choices(animmeme_list, weights=weights)[0]

    animmeme_path = os.path.join(animpath, animrandom_meme)  # абсолютный путь к выбранному изображению
    with open(animmeme_path, 'rb') as f:  # открываем файл
        bot.send_photo(message.chat.id, f)  # отправляем файл



@bot.message_handler(commands=["help"])
def helpus(message):
    bot.reply_to(
        message,
        "/set - ставит таймер\n"
        "/start - выдаёт приветствие\n"
        "/unset - удаляет таймер\n"
        "/ping - проверяет текущий пинг\n"
        "/mem - отправляет мем\n"
        "/animals - отправляет мем про животных\n"
        "/help - выдаёт данное сообщение"
    )

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Кажется, такой команды нет ☹️\n"
                 "Используйте команду /help, чтобы прочитать список доступных команд.")

if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
