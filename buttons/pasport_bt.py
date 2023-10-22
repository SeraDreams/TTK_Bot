from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

just_bt = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
true_bt = KeyboardButton("Данные верны")
just_bt.add(true_bt)
