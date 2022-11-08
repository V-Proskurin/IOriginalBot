# # это надо добавлять, чтобы просле нажатия кнопки в инлайн клавиатуре (появляется после /start)
# # мы обрабатывали ответ нажатый на клавиатуре. Не работает, если просто Жми написать текстом, только для кнопки
# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     try:
#         if call.message:
#             if call.data == "Жми":
#                 bot.send_message(call.message.chat.id, "Зачем нажал?")
#     except Exception as e:
#         print(repr(e))

# @bot.message_handler(content_types="web_app_data")  # получаем отправленные данные
# def answer(webAppMes):
#     print(webAppMes)  # вся информация о сообщении
#     print(webAppMes.web_app_data.data)  # конкретно то что мы передали в бота
#     bot.send_message(webAppMes.chat.id, f"получили инофрмацию из веб-приложения: {webAppMes.web_app_data.data}")
#     # отправляем сообщение в ответ на отправку данных из веб-приложения


# это наша старая команда, если /button отправили в чат, то появляется вопрос Выберите что вам надо и при нажатии кнопки возвращается текст Жми
# @bot.message_handler(commands=['button'])
# def button_message(message):
#     markup: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1 = types.KeyboardButton("Жми")
#     markup.add(item1)
#     bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

# это наша старая команда, если после /button или из другого места отправили Жми. Иначе возвращает на старт и показывает кнопки стартовые
# @bot.message_handler(content_types=['text'])
# def message_reply(message):
#     if message.text == "Жми":
#         bot.send_message(message.chat.id, "Зачем нажал???")
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши Привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
