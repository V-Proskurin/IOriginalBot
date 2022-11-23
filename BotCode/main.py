import telebot
import mysql.connector
from telebot import types
from telebot.types import ReplyKeyboardMarkup

# надо файл конфиг сделать https://snippcode.ru/telegram-bot-python-pytelegrambotapi
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

#добавляем пока руками пользователей в локальную БД
# sql = "INSERT INTO customers (name, last_name, first_name, user_login, user_nicename, user_email, nickname,  wptelegram_user_id, wptelegram_username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
# val = ("Вася", "Петров", "Вася", "Vtellogin", "Vtellogin", "Vtellogin@fg.ru", "Vtellogin", "95789544", "Vtellogin")
# mycursor.execute(sql, val)

# mydb.commit()

# print(mycursor.rowcount, "record inserted.")

# меняем поле wptelegram_user_id на уникальное
#mycursor.execute("ALTER TABLE customers ADD UNIQUE (wptelegram_user_id)")


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

#Пользователь отвечает и мы записываем все временно в user_dict, на втором шаге от туда забираем ID и привязываем его к фамилии
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

def process_last_name_step(message):
    try:
        user_id = message.from_user.id
        last_name = message.text
        user = user_dict[user_id]
        user.last_name = last_name

# обязательно сделать случайную генерацию почты и если вдруг такая уже есть, то сгенерировать новую.
# обязательно сделать проверку на то, что пользователь уже есть в базе и если есть, то просто даем ссылку на вход, пусть в админке все правит
# сейчас только в конце он говорит упс, типа уже такой есть в базе. А надо сразу писать
# Поле Ник майнкрафт не заполняем автоматом, делаем его уникальным в базе. пусть вводит руками и его проверяем.
# Поле ID телеграмм тоже делаем уникальным и проверяем в самом начале, что такого пользователя нет в базе
# Если его нет, только тогда начинаем спрашивать имя и фамилию. В конце кидаем в админку и предлагаем заполнить НИК майнкрафт и прочее
# Из кода убираем заполнение Ника майнкрафт.
        sql = "INSERT INTO customers (name, last_name, first_name, user_login, user_nicename, user_email, nickname, wptelegram_user_id, wptelegram_username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (user.name, user.last_name, user.name, message.from_user.username, message.from_user.username, "test@x1team.ru", message.from_user.username, user_id, message.from_user.username)
        mycursor.execute(sql, val)

        mydb.commit()

        #print(mycursor.rowcount, "record inserted.")

        msg = bot.reply_to(message, 'Спасибо!', reply_markup=webAppKeyboardInline2())
    except Exception as e:
        bot.reply_to(message, 'oooops')

def webAppKeyboardInline2():  # создание inline-клавиатуры с webapp кнопкой
    keyboard = types.InlineKeyboardMarkup(row_width=1)  # создаем клавиатуру inline
    webApp = types.WebAppInfo("https://x1team.ru/")
    one = types.InlineKeyboardButton(text="X1team.ru", web_app=webApp)  # создаем кнопку типа webapp
    # four = types.InlineKeyboardButton(text="Войти", login_url=)  # получить урл у Андрея
    keyboard.add(one)  # добавляем кнопку в клавиатуру

    return keyboard  # возвращаем клавиатуру

# Handle '/авторизоваться' '/Авторизоваться'
@bot.message_handler(commands=['авторизоваться', 'Авторизоваться'])
def send_welcome(message):
    user_id = message.from_user.id
    sql = "SELECT * FROM customers WHERE wptelegram_user_id = %s"
    adr = (user_id, )
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    if myresult == "":
        msg = bot.reply_to(message, "Как Вас зовут?")
        bot.register_next_step_handler(msg, process__name_step)
    else:
        msg = bot.reply_to(message, 'Такой пользователь уже существует! Войдите на сайт по ссылке', reply_markup=webAppKeyboardInline2())

# Это какое-то кэширование. Записывает в файл. Возможно надо чистить, а то завалит память мусором.
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
