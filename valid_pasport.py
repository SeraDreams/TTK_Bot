import os

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from create_bot import bot
from pro_pasport import recognize_passport
from buttons.keyboard import keyboard_select
import db.db_connect as db
from ticket import FindTicketData

class PassportTicket(StatesGroup):
    passport = State()
    ticket = State()
    select = State()


async def start(message: types.Message):
    user_id = message.from_user.id
    if db.check_tg_user(user_id):
        await bot.send_message('Привет! Я ТЕБЯ БЛЯТЬ ЗНАЮ!')
        await PassportTicket.select.set()
    else:
        await bot.send_message('Привет! Я ТЕБЯ БЛЯТЬ Запомнил!')
        await PassportTicket.select.set()


async def recognition_selection():
    await bot.send_message('выбери что будем проверякать', reply_markup=keyboard_select)


async def ticket(message: types.Message, state: FSMContext):
    await bot.send_message('Отправь билет')


async def get_ticket(message: types.Message, state: FSMContext):
    # FindTicketData
    user_id = message.from_user.id
    await message.photo[-1].download(destination_file=f"check_img/{user_id}.jpg")

    data = FindTicketData(filepath=f"check_img/{user_id}t.jpg").start()
    os.remove(f"check_img/{user_id}.jpg")
    getticket = db.get_passenger_info(ticket_num=data)
    if getticket:
        await bot.send_message(f'билета eсть в базе вот вваши данные \n {getticket}')
    else:
        await bot.send_message('билета нету в базе')


async def passport(message: types.Message, state: FSMContext):
    await bot.send_message('Отправь паспорт')


async def get_passport(message: types.Message, state: FSMContext):
    # FindTicketData
    user_id = message.from_user.id
    await message.photo[-1].download(destination_file=f"passport_img/{user_id}.jpg")

    data = recognize_passport(f"passport_img/{user_id}.jpg", user_id)
    os.remove(f"passport_img/{user_id}.jpg")
    getticket = db.get_passenger_info(passport=data['Номер']+data['Серия'])
    if getticket:
        await bot.send_message(f'паспорт eсть в базе вот вваши данные \n {getticket}')
    else:
        await bot.send_message('паспорт нету в базе')


# async def passport_start(message: types.Message):
#     await bot.send_photo(photo=open("img.png", "rb"), chat_id=message.from_user.id, caption="Отправьте фото паспорта, по такому примеру")
#     await PassportImg.img.set()
#
#
# async def take_passport_img(message: types.Message, state: FSMContext):
#     async with state.proxy() as q:
#         id = message.from_user.id
#         await message.photo[-1].download(destination_file=f"user_pasport/{id}.jpg")
#
#         global data
#         global reply_answer
#         delete = await message.reply('Фото обрабатывается')
#         data = recognize_passport(f"user_pasport/{id}.jpg", id)
#         answer_text = f"<b>Пожалуйста проверти данные:</b>\nИмя - {data['Имя']}\nФамилия - {data['Фамилия']}\nОтчество - {data['Отчество']}\nНомер - {data['Номер']}\nСерия - {data['Серия']}\n\nЧтобы изменить данные отправьте Пункт - На какое значение изменить"
#         await delete.delete()
#         reply_answer = await message.answer(answer_text, parse_mode="HTML", reply_markup=just_bt)
#         await state.finish()
#
#
# async def edit_data(message: types.Message):
#     try:
#         msg = message.text
#         print(msg.split('-')[0].replace(" ", ""), data.keys())
#         if msg.split('-')[0].replace(" ", "") in data.keys():
#             data[msg.split('-')[0].replace(" ", "")] = msg.split('-')[1].replace(" ", "")
#             await message.reply("Значение успешно обновлено!")
#             answer_text = f"<b>Пожалуйста проверти данные:</b>\nИмя - {data['Имя']}\nФамилия - {data['Фамилия']}\nОтчество - {data['Отчество']}\nНомер - {data['Номер']}\nСерия - {data['Серия']}\n\nЧтобы изменить данные отправьте Пункт - На какое значение изменить"
#             await message.answer(answer_text, parse_mode="HTML", reply_markup=just_bt)
#         elif msg == "Данные верны":
#             # Сохранение в БД или куда там блять надо
#             await message.answer("Меню:")
#         elif msg.count('-') == 1:
#             await message.reply("Такого пункта не сушествует")
#     except:
#         pass
#
#




def reg_hand_valid_passport(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(recognition_selection, state=PassportTicket.select)
    dp.register_message_handler(ticket, state=PassportTicket.ticket)
    dp.register_message_handler(ticket, state=PassportTicket.ticket, content_types=['photo'])
    dp.register_message_handler(passport, state=PassportTicket.passport)
    dp.register_message_handler(passport, state=PassportTicket.passport, content_types=['photo'])
