import time
import threading
import schedule
import telebot
import os
import random

API_TOKEN = 'token'
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

@bot.message_handler(commands=['recyclingadvice'])
def send_recycle_tip(message):
    tips = [
        "Пластик отправляйте в контейнер для переработки только чистым.",
        "Стекло можно переработать, но его важно не разбивать перед сдачей.",
        "Используйте многоразовые сумки, чтобы снизить потребление пластика.",
        "Старайтесь выбирать товары без излишней упаковки.",
        "Одежду, которую вы больше не носите, сдайте на переработку или в благотворительные организации.",
        "Избегайте покупки пластиковых бутылок — вместо этого используйте многоразовые бутылки для воды.",
        "Сдавайте использованные батарейки и электронику в специальные пункты приема, а не в мусорное ведро.",
        "Используйте стеклянные и металлические банки повторно, например, для хранения продуктов или мелочей.",
        "При компостировании отходов добавляйте не только овощные очистки, но и яичную скорлупу, кофейную гущу и листовой чай.",
        "Не выбрасывайте старые книги и журналы — их можно отдать в библиотеки, школы или благотворительные организации.",
        "Перед покупкой новых вещей подумайте, можно ли найти аналог из переработанных материалов.",
        "Покупайте продукты и бытовые товары на развес, чтобы избежать лишней упаковки.",
        "Проверьте, принимает ли ваш город тетрапак на переработку, и сдавайте упаковку только чистой.",
        "Не выбрасывайте текстиль вместе с бытовыми отходами — сдайте его на переработку.",
        "Старайтесь избегать одноразовых пластиковых изделий, таких как вилки, ложки и соломинки.",
        "Если у вас есть ненужная техника, попробуйте отдать ее в ремонт или продать, прежде чем выбрасывать.",
        "При покупке товаров отдавайте предпочтение тем, чья упаковка подлежит переработке.",
        "Используйте старые газеты и картон для создания компоста или для домашних поделок.",
        "Старайтесь покупать многоразовые контейнеры для хранения продуктов вместо одноразовых пакетов.",
        "Собирайте и перерабатывайте металлические крышки от банок и бутылок."

        # советы чатгпт генерировал
    ]
    bot.reply_to(message, random.choice(tips))


@bot.message_handler(commands=["help"])
def helpus(message):
    bot.reply_to(
        message,
        "/start - выдаёт приветствие\n"
        "/set - ставит таймер\n"
        "/unset - удаляет таймер\n"
        "/ping - проверяет текущий пинг\n"
        "/mem - отправляет мем\n"
        "/animals - отправляет мем про животных\n"
        "/recyclingadvice - получить совет по переработке мусора\n"
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
