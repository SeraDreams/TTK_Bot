from aiogram import executor
from create_bot import dp
from config import on_startup
import valid_pasport

valid_pasport.reg_hand_valid_passport(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
