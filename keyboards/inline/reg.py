from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

reg = InlineKeyboardMarkup(row_width=1)

btn1 = InlineKeyboardButton(text='Начать регистрацию', callback_data='start_reg')

reg.add(btn1)