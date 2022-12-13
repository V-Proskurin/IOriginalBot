import telebot
import mysql.connector
from telebot import types
from telebot.types import ReplyKeyboardMarkup

# !!!!! надо файл конфиг сделать https://snippcode.ru/telegram-bot-python-pytelegrambotapi
token = '5437003366:AAGxz3jzfF8YlWlJGe47bz1QJAKddeLFxNE'
bot = telebot.TeleBot(token)

mydb = mysql.connector.connect(
  host="localhost",
  user="bot",
  password="bot123",
  port="3306",
  database="wp_base"
)
mycursor = mydb.cursor()


## !!!!! https://python-scripts.com/requests разобраться как работает

# проверка, что к базе подключился
#print(mydb)

# Как работать с БД https://www.w3schools.com/python/python_mysql_where.asp

#создали БД
#mycursor.execute("CREATE DATABASE wp_base")

# Надо новых две создать таблицы
# wp_usermeta: nickname (VVP игровой ник), first_name (Виктор - заполняем и смотрим в телеге, если есть), last_name (Проскурин заполняем тем, что есть в телеге, если нет, ставим пусто), wptelegram_user_id (заполняем), wptelegram_username (VVProskurin), billing_first_name (Виктор заполняем из телеги), billing_last_name (Проскурин заполняем из телеги), billing_email (генерим)
# и взять все по максимум из телеграмм https://core.telegram.org/bots/api#user

#создаем таблицу 1
#в таблице обязательно делаем ключ: primary key - номер записи автоматический и добавляем другие поля
# wp_users: user_login (vvproskurin логин несменяемый); user_nicename (vvproskurin не используем, но заполняем); user_email (генерим случайный), display_name (vvproskurin заполняем)
#mycursor.execute("CREATE TABLE wp_users (id INT AUTO_INCREMENT PRIMARY KEY, user_login VARCHAR(60), user_nicename VARCHAR(50), user_email VARCHAR(100), display_name VARCHAR(250))")

#создаем таблицу 2
#mycursor.execute("CREATE TABLE wp_usermeta (id INT AUTO_INCREMENT PRIMARY KEY, user_id BIGINT(20), meta_key VARCHAR(255), meta_value LONGTEXT)")

#сохраняем данные пользователя вначале в программе как в примере пошагового бота https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/step_example.py
user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.last_name = None

# Добавляем любого пользователя в вордпресс при заходе по старту. Сразу  регистрируем.
# С сайтом может работать несколько ботов, поэтому не у бота пользователей храним, а на сайте.
# Дальше при любом входе к боту смотрим у бота он был недавно?, если нет, то смотрим в базе, если пользователя нет в базе вордпресс, то добавляем его в базу с ФИО и данными из телеги
# Когда ему надо будет он потом по ссылке зайдет в ЛК и поправит ФИО, телефон, почту, адреса и прочее
# !!!! wptelegram_user_id это не поле, а значение. Уникальным сделать нельзя. Поэтому обязательная проверка перед добавлением
# !!!! Проверяем на бота и если бот, то не регестрируем message.from_user.is_bot
# !!!! Всегда проверяем у бота он был недавно? После проверки в базе данных и записи ее надо закончить, записав в сеанс переменную, что недавно был и не проверять повторно. Потом можно сеанс очистить. Это нужно, если вдруг из базы сайта его удалили, чтобы заново добавить
# !!!! Генерим почту
# !!!! разобраться как на мультисайт его добавлять, чтобы и там числился

# !!!!!! Как вообще правильно? Задача проверить есть ли в таблице wp_usermeta в столбце meta_key со значением wptelegram_user_id пользователь с конкретным значением равнум его id, который телега отдает: message.from_user.id
# Есть статья https://misha.agency/wordpress/interfacing-with-the-database.html
# И еще мануал простой Как работать с БД https://www.w3schools.com/python/python_mysql_where.asp
# Я по нему начал учиться:
# sql = "SELECT * FROM wp_usermeta WHERE meta_key = wptelegram_user_id and meta_value = user_id" Так можно?
# Но надо, чтобы как в примере с параметром для безопасности WHERE meta_key = %s:
# sql = "SELECT * FROM wp_usermeta WHERE meta_key = %s"
# meta_key = ("wptelegram_user_id", )
# mycursor.execute(sql, meta_key)
# myresult = mycursor.fetchall()
# for x in myresult:
#   if ....... и как дальше?

# wp_users: user_login (vvproskurin логин несменяемый); user_nicename (vvproskurin не используем, но заполняем); user_email (генерим случайный), display_name (vvproskurin заполняем)
# wp_usermeta: nickname (VVP игровой ник), first_name (Виктор - заполняем и смотрим в телеге, если есть), last_name (Проскурин заполняем тем, что есть в телеге, если нет, ставим пусто), wptelegram_user_id (заполняем), wptelegram_username (VVProskurin), billing_first_name (Виктор заполняем из телеги), billing_last_name (Проскурин заполняем из телеги), billing_email (генерим)

# Это проверка:
# @bot.message_handler(func=lambda message: True)
# def check_user(message):
#     try:
#         user_id = message.from_user.id
#         sql = "SELECT * FROM wp_usermeta WHERE wptelegram_user_id = %s"
#         adr = (user_id, )
#         mycursor.execute(sql, adr)
#         myresult = mycursor.fetchall()
#         if myresult != []:
#             user_id = message.from_user.id
#         else:

#             sql = "INSERT INTO customers (name, last_name, first_name, user_login, user_nicename, user_email, nickname, wptelegram_user_id, wptelegram_username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#             val = (user.name, user.last_name, user.name, message.from_user.username, message.from_user.username, "test@x1team.ru", message.from_user.username, user_id, message.from_user.username)
#             mycursor.execute(sql, val)
#             mydb.commit()

#     except Exception as e:
#         print(repr(e))


# Эта клавиатура появляется при старте. Сюда надо добавить кнопку для авторизации на сайте, разобраться как работает
# https://t.me/x1test1Bot вот здесь описание

def webAppKeyboardInline():  # создание inline-клавиатуры с webapp кнопкой
    keyboard = types.InlineKeyboardMarkup(row_width=1)  # создаем клавиатуру inline
    login_url = types.LoginUrl(url = "https://x1team.ru?action=wptelegram_login", request_write_access = True)
    #webApp = types.WebAppInfo("https://x1team.ru?action=wptelegram_login")
    webApp2 = types.WebAppInfo("https://telegram.mihailgok.ru") # создаем webappinfo - формат хранения url https://telegram.mihailgok.ru
    webAppGame = types.WebAppInfo("https://demos.gleamtech.com/filevista/")  # создаем webappinfo - формат хранения url
    one = types.InlineKeyboardButton(text="X1team.ru", login_url=login_url)  # создаем кнопку типа login_url
    #one = types.InlineKeyboardButton(text="X1team.ru", web_app=webApp)  # создаем кнопку типа webapp
    two = types.InlineKeyboardButton(text="Игра", web_app=webAppGame)  # создаем кнопку типа webapp
    three = types.InlineKeyboardButton(text="Регистрация", callback_data="Регистрация")  # работает, не запускает команду
    four = types.InlineKeyboardButton(text="Твои данные на сайте", web_app=webApp2)
    # four = types.InlineKeyboardButton(text="Войти", login_url=)  # получить урл у Андрея
    keyboard.add(one, two, three, four)  # добавляем кнопку в клавиатуру

    return keyboard  # возвращаем клавиатуру

# !!! Надо добавление в базу сделать на старте и проверку на наличие в базе. Если есть даем ссылку на ЛК для правки ФИО, телефона, адреса доставки
@bot.message_handler(commands=['start'])  # обрабатываем команду старт
def start_fun(message):
    bot.send_message(message.chat.id, 'Привет, ✌️")\nНажми на кнопки внизу.', parse_mode="Markdown",
                     reply_markup=webAppKeyboardInline())  # отправляем сообщение c нужной клавиатурой

# Если нажал в первой клавиатуре Регистрация, то выполняем логику авторизоваться и после Имя бросаем на второй шаг
# инструкция пощагового бота https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/step_example.py
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "Регистрация" or "регистрация":
                msg = bot.send_message(call.message.chat.id, "Введите имя")
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
        bot.reply_to(message, 'Что то пошло не так, попробуйте еще раз, пожалуйста')

def process_last_name_step(message):
    try:
        user_id = message.from_user.id
        last_name = message.text
        user = user_dict[user_id]
        user.last_name = last_name

# обязательно сделать случайную генерацию почты и если вдруг такая уже есть, то сгенерировать новую.
# Из кода убираем заполнение Ника майнкрафт. Пусть вводит руками на сайте, когда играть захочет.
# Даем ссылку на ЛК. Пусть там все редактирует.
        sql = "INSERT INTO wp_users (user_login, user_nicename, user_email, display_name ) VALUES (%s, %s, %s, %s)"
        val = (message.from_user.username, message.from_user.username, 123, message.from_user.username)
        mycursor.execute(sql, val)

        mydb.commit()

        #print(mycursor.rowcount, "record inserted.")

        msg = bot.reply_to(message, 'Спасибо!', reply_markup=webAppKeyboardInline2())
    except Exception as e:
        bot.reply_to(message, 'Что то пошло не так, попробуйте еще раз, пожалуйста!!!')

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
    if myresult != []:
        msg = bot.reply_to(message, 'Такой пользователь уже существует! Войдите на сайт по ссылке', reply_markup=webAppKeyboardInline2())
    else:
        msg = bot.reply_to(message, "Как Вас зовут?")
        bot.register_next_step_handler(msg, process__name_step)


# Это какое-то кэширование. Записывает в файл. Возможно надо чистить, а то завалит память мусором.
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
