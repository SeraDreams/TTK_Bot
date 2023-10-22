from aiogram import executor
from create_bot import dp
import valid_pasport

from db.db_connect import prepare_tables

valid_pasport.reg_hand_valid_passport(dp)


async def on_startup(dp):
    prepare_tables()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
