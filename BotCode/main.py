import telebot
import mysql.connector
from telebot import types
from telebot.types import ReplyKeyboardMarkup

token = '5246882341:AAHdcgZKCKvytKWR1-IyP8Pl6jkmBiIcJRU'
bot = telebot.TeleBot(token)

mydb = mysql.connector.connect(
  host="localhost",
  user="bot",
  password="bot123",
  port="3306",
  database="botdb"
)
# проверка, что к базе подключился
#print(mydb)

#создаем БД
mycursor = mydb.cursor()
#создали БД
#mycursor.execute("CREATE DATABASE botdb")

#создаем таблицу
#mycursor.execute("CREATE TABLE customers (name VARCHAR(255), last_name VARCHAR(255))")

#в таблице обязательно делаем ключ: primary key - номер записи автоматический и добавляем другие поля
#mycursor.execute("ALTER TABLE customers ADD COLUMN (id INT AUTO_INCREMENT PRIMARY KEY, user_login VARCHAR(255), user_nicename VARCHAR(255), user_email VARCHAR(255), nickname VARCHAR(255), first_name VARCHAR(255), wptelegram_user_id INT, wptelegram_username VARCHAR(255))")

#сохраняем данные пользователя вначале в программе как в примере пошагового бота https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/step_example.py
user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.last_name = None

# Эта клавиатура появляется при старте. Сюда надо добавить кнопку для авторизации на сайте, разобраться как работает
# https://t.me/x1test1Bot вот здесь описание

def webAppKeyboardInline():  # создание inline-клавиатуры с webapp кнопкой
    keyboard = types.InlineKeyboardMarkup(row_width=1)  # создаем клавиатуру inline
    webApp = types.WebAppInfo("https://x1team.ru/")
    webApp2 = types.WebAppInfo("https://telegram.mihailgok.ru") # создаем webappinfo - формат хранения url https://telegram.mihailgok.ru
    webAppGame = types.WebAppInfo("https://games.mihailgok.ru")  # создаем webappinfo - формат хранения url
    one = types.InlineKeyboardButton(text="X1team.ru", web_app=webApp)  # создаем кнопку типа webapp
    two = types.InlineKeyboardButton(text="Игра", web_app=webAppGame)  # создаем кнопку типа webapp
    three = types.InlineKeyboardButton(text="Авторизоваться", callback_data="Авторизоваться")  # работает, не запускает команду
    four = types.InlineKeyboardButton(text="Твои данные на сайте", web_app=webApp2)
    # four = types.InlineKeyboardButton(text="Войти", login_url=)  # получить урл у Андрея
    keyboard.add(one, two, three, four)  # добавляем кнопку в клавиатуру

    return keyboard  # возвращаем клавиатуру


@bot.message_handler(commands=['start'])  # обрабатываем команду старт
def start_fun(message):
    bot.send_message(message.chat.id, 'Привет, ✌️")\nНажми на кнопки внизу.', parse_mode="Markdown",
                     reply_markup=webAppKeyboardInline())  # отправляем сообщение c нужной клавиатурой


# Если нажал в первой клавиатуре Авторизоваться, то выполняем логику авторизоваться и после Имя бросаем на второй шаг
# инструкция пощагового бота https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/step_example.py
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "Авторизоваться" or "авторизоваться":
                msg = bot.send_message(call.message.chat.id, "Как Вас зовут?")
                bot.register_next_step_handler(msg, process__name_step)
    except Exception as e:
        print(repr(e))


# Handle '/авторизоваться' '/Авторизоваться'
@bot.message_handler(commands=['авторизоваться', 'Авторизоваться'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Как Вас зовут?
""")
    bot.register_next_step_handler(msg, process__name_step)

# Пользователь отвечает и мы записываем все в user_dict
def process__name_step(message):
    try:
        # chat_id = message.chat.id вместо номера чата поставим номер пользователя
        user_id = message.from_user.id
        name = message.text
        user = User(name)
        user_dict[user_id] = user
        msg = bot.reply_to(message, "Введите фамилию")
        bot.register_next_step_handler(msg, process_last_name_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def webAppKeyboardInline2():  # создание inline-клавиатуры с webapp кнопкой
    keyboard = types.InlineKeyboardMarkup(row_width=1)  # создаем клавиатуру inline
    webApp = types.WebAppInfo("https://x1team.ru/")
    one = types.InlineKeyboardButton(text="X1team.ru", web_app=webApp)  # создаем кнопку типа webapp
    # four = types.InlineKeyboardButton(text="Войти", login_url=)  # получить урл у Андрея
    keyboard.add(one)  # добавляем кнопку в клавиатуру

    return keyboard  # возвращаем клавиатуру

def process_last_name_step(message):
    try:
        user_id = message.from_user.id
        last_name = message.text
        user = user_dict[user_id]
        user.last_name = last_name
        msg = bot.reply_to(message, 'Спасибо!', reply_markup=webAppKeyboardInline2())
    except Exception as e:
        bot.reply_to(message, 'oooops')



# Это какое-то кэширование. Записывает в файл. Возможно надо чистить, а то завалит память мусором.
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
