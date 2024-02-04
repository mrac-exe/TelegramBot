#6950572451:AAG07IBQCc48KykHdwSTRiSZVzT8t_vHbF8

import telebot
from telebot import types
from currency_converter import CurrencyConverter

TOKEN = ('6950572451:AAG07IBQCc48KykHdwSTRiSZVzT8t_vHbF8')

bot = telebot.TeleBot(TOKEN)
currency = CurrencyConverter()
amount = 0

# Обрабатываются сообщение команды '/start'.
@bot.message_handler(commands=['start'])
def handle_start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name}, введите сумму нужной валюты")
    bot.register_next_step_handler(message, summ)

# Обрабатываются сообщение команды '/help'.
@bot.message_handler(commands=['help'])
def handle_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, я умею показывать курсы валют, "
                                      f"для этодо достаточно просто ввести сумму валюты и выбрать две валюты или выбрать другие")

def summ(message):
    global amount
    # преобразование сообщения в целое числo
    try:
        amount = int(message.text.strip())
    # Если возникнет ошибка, отправьте сообщение об ошибке и отправить сообщение для повторного ввода суммы
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректно введино число. Введите сумму')
        bot.register_next_step_handler(message,summ)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width= 2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup= markup)
    # Если сумма меньше или равна нулю, отправьте сообщение об ошибке и попросите повторного ввода суммы
    else:
        bot.send_message(message.chat.id, 'Сумма должна быть больше 0. Введите сумму')
        bot.register_next_step_handler(message, summ)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        # Получаем данные из колбэка и делим их на две валюты
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получилось:{round(res, 2)}. Можете впишисать сумму снова')
        bot.register_next_step_handler(call.message, summ)
    else:
        bot.send_message(call.message.chat.id, "Введите два валюты через / , например: 'USD/JPY")
        bot.register_next_step_handler(call.message, my_currency)

#  пишем обработчик для значения другие валюты
def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получилось:{round(res, 2)}. Можете впишисать сумму снова')
        bot.register_next_step_handler(message, summ)
    except Exception:
        bot.send_message(message.chat.id, f'Что-то не так, впишите значение снова')
        bot.register_next_step_handler(message, my_currency)

bot.polling(none_stop=True)
