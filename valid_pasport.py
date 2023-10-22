from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from create_bot import bot
from pro_pasport import recognize_passport
from buttons.pasport_bt import just_bt


class PassportImg(StatesGroup):
    img = State()


async def passport_start(message: types.Message):
    await bot.send_photo(photo=open("img.png", "rb"), chat_id=message.from_user.id, caption="Отправьте фото паспорта, по такому примеру")
    await PassportImg.img.set()


async def take_passport_img(message: types.Message, state: FSMContext):
    async with state.proxy() as q:
        id = message.from_user.id
        await message.photo[-1].download(destination_file=f"user_pasport/{id}.jpg")

        global data
        global reply_answer
        delete = await message.reply('Фото обрабатывается')
        data = recognize_passport(f"user_pasport/{id}.jpg", id)
        answer_text = f"<b>Пожалуйста проверти данные:</b>\nИмя - {data['Имя']}\nФамилия - {data['Фамилия']}\nОтчество - {data['Отчество']}\nНомер - {data['Номер']}\nСерия - {data['Серия']}\n\nЧтобы изменить данные отправьте Пункт - На какое значение изменить"
        await delete.delete()
        reply_answer = await message.answer(answer_text, parse_mode="HTML", reply_markup=just_bt)
        await state.finish()


async def edit_data(message: types.Message):
    try:
        msg = message.text
        print(msg.split('-')[0].replace(" ", ""), data.keys())
        if msg.split('-')[0].replace(" ", "") in data.keys():
            data[msg.split('-')[0].replace(" ", "")] = msg.split('-')[1].replace(" ", "")
            await message.reply("Значение успешно обновлено!")
            answer_text = f"<b>Пожалуйста проверти данные:</b>\nИмя - {data['Имя']}\nФамилия - {data['Фамилия']}\nОтчество - {data['Отчество']}\nНомер - {data['Номер']}\nСерия - {data['Серия']}\n\nЧтобы изменить данные отправьте Пункт - На какое значение изменить"
            await message.answer(answer_text, parse_mode="HTML", reply_markup=just_bt)
        elif msg == "Данные верны":
            # Сохранение в БД или куда там блять надо
            await message.answer("Меню:")
        elif msg.count('-') == 1:
            await message.reply("Такого пункта не сушествует")
    except:
        pass


def reg_hand_valid_passport(dp: Dispatcher):
    dp.register_message_handler(passport_start, commands=['start'])
    dp.register_message_handler(take_passport_img, content_types=['photo'], state=PassportImg.img)
    dp.register_message_handler(edit_data)
