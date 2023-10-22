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


async def start(message: types.Message, state: FSMContext):
    await state.finish()

    user_id = message.from_user.id
    if db.check_tg_user(user_id):
        await message.answer('Привет! Я тебя знаю!')
        await message.answer('Выбери что будем проверять', reply_markup=keyboard_select)
        await PassportTicket.select.set()
    else:
        await message.answer('Привет! Я тебя не знаю!')
        await message.answer('Выбери что будем проверять', reply_markup=keyboard_select)
        await PassportTicket.select.set()


async def ticket_or_passport(message: types.Message, state: FSMContext):
    await state.update_data(select=message.text)
    # получаем сохранённое состояние
    state_data = await state.get_data()

    if state_data['select'] == 'Билет':
        await message.answer('Отправь билет')
        await PassportTicket.ticket.set()
    elif state_data['select'] == 'Паспорт':
        await message.answer('Отправь паспорт')
        await PassportTicket.passport.set()


async def get_ticket(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        await message.photo[-1].download(destination_file=f"check_img/{user_id}.jpg")

        data = FindTicketData(filepath=f"check_img/{user_id}.jpg").start()
        os.remove(f"check_img/{user_id}.jpg")
        info_using_ticket = db.get_passenger_info(ticket_num=data)

        print(data)
        if info_using_ticket:
            await message.answer(f'''Билет eсть в базе, вот ваши данные
            Поезд: {info_using_ticket['train']}
            Номер вагона: {info_using_ticket['num_carriage']}
            Тип вагона: {info_using_ticket['type_carriage']}
            Место: {info_using_ticket['place']}''')
            db.add_tg_user(tg_id=user_id, rzd_user=info_using_ticket["id"])
        else:
            await message.answer('Билета нету в базе')
    except Exception as e:
        print(e)
    await state.finish()


async def get_passport(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        await message.photo[-1].download(destination_file=f"passport_img/{user_id}.jpg")

        data = recognize_passport(f"passport_img/{user_id}.jpg", user_id)
        os.remove(f"passport_img/{user_id}.jpg")
        info_using_passport = db.get_passenger_info(passport=data['Серия']+data['Номер'])

        print(data)
        if info_using_passport:
            await message.answer(f'''Паспорт eсть в базе, вот ваши данные
    Поезд: {info_using_passport['train']}
    Номер вагона: {info_using_passport['num_carriage']}
    Тип вагона: {info_using_passport['type_carriage']}
    Место: {info_using_passport['place']}''')
            db.add_tg_user(tg_id=user_id, rzd_user=info_using_passport["id"])
        else:
            await message.answer('Паспорта нету в базе')
    except Exception as e:
        print(e)
    await state.finish()


def reg_hand_valid_passport(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(ticket_or_passport, state=PassportTicket.select)
    dp.register_message_handler(get_ticket, state=PassportTicket.ticket, content_types=['photo'])
    dp.register_message_handler(get_passport, state=PassportTicket.passport, content_types=['photo'])
