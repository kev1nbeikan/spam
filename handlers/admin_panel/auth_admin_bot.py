from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telethon.errors import SessionPasswordNeededError

from data import PHONE_ADMINBOT
from data.strings import CommandsStrings, AdminPanelStrings, SUCCESS_STRING, MISS
from keyboard.callbackdata import delete_bot_data, connect_bot_data
from keyboard.markup import miss
from loader import dp, admin_bot, sessions_db
from handlers.states import AuthAdminBotStates


@dp.message_handler(Command('asd'))
async def show_admins_bot(message: types.Message):
    for session in sessions_db.get_all_by_dir_through_session_handle('admin'):
        button = InlineKeyboardMarkup()
        button.row(
            InlineKeyboardButton(AdminPanelStrings.DELETE_BOT,
                                 callback_data=delete_bot_data.new(file_name=session.name)),
            InlineKeyboardButton(AdminPanelStrings.CONNECT_BOT,
                                 callback_data=connect_bot_data.new(file_name=session.name)),
        )
        await message.answer(text=session.name, reply_markup=button)


@dp.callback_query_handler(delete_bot_data.filter())
async def delete_adminbot(call: types.CallbackQuery, callback_data: dict):
    session = sessions_db.get_one_through_session_handle(folder='admin', name=callback_data['file_name'])
    session.delete(from_files=True, from_db=True)
    await call.answer(SUCCESS_STRING)


@dp.message_handler(Command(CommandsStrings.AUTH))
async def connect_adminbot(message: types.Message, state: FSMContext):
    if not await admin_bot.is_user_authorized():
        sentcode = await admin_bot.send_code_request(PHONE_ADMINBOT)
        await state.update_data(phone_code_hash=sentcode.phone_code_hash)
        await message.answer(AdminPanelStrings.ASK_CODE)
        await AuthAdminBotStates.wait_code.set()


@dp.message_handler(state=AuthAdminBotStates.wait_code)
async def get_code(message: types.Message, state: FSMContext):
    await state.update_data(code=message.text)
    await message.answer(AdminPanelStrings.ASK_IF_NEED_PASSWORD, reply_markup=miss)
    await AuthAdminBotStates.wait_password.set()


@dp.message_handler(state=AuthAdminBotStates.wait_password)
async def sign_in_adminbot(message: types.Message, state: FSMContext):
    if MISS == message.text:
        await state.update_data(password=message.text)
    async with state.proxy() as data:
        try:
            await admin_bot.sign_in(
                phone_code_hash=data['phone_code_hash'],
                code=data['code']
            )
            await message.answer(SUCCESS_STRING)
        except SessionPasswordNeededError:
            if 'password' not in data:
                message.text = data['code']
                await get_code(message, state)
                return
            await admin_bot.sign_in(
                phone_code_hash=data['phone_code_hash'],
                password=data['password'] if 'password' in data else None,
                code=data['code']
            )
            await message.answer(SUCCESS_STRING)








