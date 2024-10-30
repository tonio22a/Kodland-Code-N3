import time
import threading
import schedule
import telebot

API_TOKEN = '7876584346:AAHId83U9P5u0faYAsZEmjOu_5wnWldh74c'
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! используйте /help для того, чтобы прочитать список команд")


def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Таймер!')


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


@bot.message_handler(commands=["help"])
def helpus(message):
    bot.reply_to(
        message,
        "/set - ставит таймер\n"
        "/start - выдаёт приветствие\n"
        "/unset - удаляет таймер\n"
        "/ping - проверяет текущий пинг\n"
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
