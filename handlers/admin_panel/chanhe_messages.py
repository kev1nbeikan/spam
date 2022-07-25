from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import CantParseEntities

from data import StartMenuStrings
from loader import dp, message_db
from keyboard import change_msg_data
from aiogram import types
from aiogram.utils import markdown as fmt
from handlers.states import AdminChangeMessage
from handlers.filters import  IsAdminFilter

@dp.callback_query_handler(change_msg_data.filter(), state='*')
async def ask_section(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    section = message_db.get_section(callback_data['section'])
    await AdminChangeMessage.wait_text.set()
    requires = section.requires.split()
    await state.update_data(requires=requires, section=section.section)
    await call.message.answer(text=f'Нужные {{поля}}: {section.requires if section.requires else "<b>отсутствуют</b>"}. Введите текст')
    await call.answer()


async def check_html(message: types.Message, text):
    try:
        msg = await message.answer(text)
        return True
    except CantParseEntities:
        return False





@dp.message_handler(IsAdminFilter(), state=AdminChangeMessage.wait_text)
async def change_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        requires = data['requires']
        section = data['section']
    text = message.text

    if not await check_html(message, text):
        await message.answer(text='неверные теги')
        return

    if all((r in text for r in requires)) or not requires:
        message_db.update_section(section=section, text=text)
        await message.answer(text='успешно')
        await state.finish()
    else:
        await message.answer(text='нет всех полей')






