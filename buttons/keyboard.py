from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

commands = [
    'Билет', 'Паспорт',
]
keyboard_select = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
keyboard_select.row(KeyboardButton(commands[0]), KeyboardButton(commands[1]))