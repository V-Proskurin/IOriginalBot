import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup

token = '5246882341:AAHdcgZKCKvytKWR1-IyP8Pl6jkmBiIcJRU'
bot = telebot.TeleBot(token)

# в терминале пишем pip install pytelegrambotapi вначале и только после этого запускаем программу. Если выдает ошибку
# то удаляем установку вначале pip uninstall telebot , а затем pip uninstall pytelegrambotapi
# и заново пишем pip install pytelegrambotapi - тогда файл запускается и все работает.

# Эта клавиатура появляется при старте. Сюда надо добавить кнопку для авторизации на сайте, разобраться как работает
# https://t.me/x1test1Bot вот здесь описание

def webAppKeyboardInline():  # создание inline-клавиатуры с webapp кнопкой
    keyboard = types.InlineKeyboardMarkup(row_width=1)  # создаем клавиатуру inline
    webApp = types.WebAppInfo("https://telegram.mihailgok.ru")  # создаем webappinfo - формат хранения url
    webAppGame = types.WebAppInfo("https://games.mihailgok.ru")  # создаем webappinfo - формат хранения url
    one = types.InlineKeyboardButton(text="Веб приложение", web_app=webApp)  # создаем кнопку типа webapp
    two = types.InlineKeyboardButton(text="Игра", web_app=webAppGame)  # создаем кнопку типа webapp
    three = types.InlineKeyboardButton(text="Жми", callback_data="Жми")  # работает
   # four = types.InlineKeyboardButton(text="Войти", login_url=)  # получить урл
    keyboard.add(one, two, three)  # добавляем кнопку в клавиатуру

    return keyboard  # возвращаем клавиатуру


@bot.message_handler(commands=['start'])  # обрабатываем команду старт
def start_fun(message):
    bot.send_message(message.chat.id, 'Привет, ✌️")\nНажми на кнопки внизу.', parse_mode="Markdown",
                     reply_markup=webAppKeyboardInline())  # отправляем сообщение c нужной клавиатурой


@bot.message_handler(content_types="web_app_data")  # получаем отправленные данные
def answer(webAppMes):
    print(webAppMes)  # вся информация о сообщении
    print(webAppMes.web_app_data.data)  # конкретно то что мы передали в бота
    bot.send_message(webAppMes.chat.id, f"получили инофрмацию из веб-приложения: {webAppMes.web_app_data.data}")
    # отправляем сообщение в ответ на отправку данных из веб-приложения

# это наша старая команда, если /button отправили в чат, то появляется вопрос Выберите что вам надо и при нажатии кнопки возвращается текст Жми
@bot.message_handler(commands=['button'])
def button_message(message):
    markup: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Жми")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

# это наша старая команда, если после /button или из другого места отправили Жми. Иначе возвращает на старт и показывает кнопки стартовые
@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "Жми":
        bot.send_message(message.chat.id, "Зачем нажал?")
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

# это надо добавлять, чтобы просле нажатия кнопки в инлайн клавиатуре (появляется после /start)
# мы обрабатывали ответ нажатый на клавиатуре
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "Жми":
                bot.send_message(call.message.chat.id, "Зачем нажал?")
            if call.data == "bad":
                bot.send_message(call.message.chat.id, "Ничего, все наладится!")
    except Exception as e:
        print(repr(e))


bot.infinity_polling()
