from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from data import CommandsStrings, StartMenuStrings
from loader import dp, users_db
from keyboard import start_menu
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from misc.db_api import User
from data import GettingMessageStrings


# @dp.message_handler(content_types=ContentType.ANY)
# async def echo(message: types.Message):
#     await message.answer(message.photo[0].file_id)

@dp.message_handler(Command(CommandsStrings.START), state='*')
async def menu(message: types.Message, state: FSMContext):
    user = User(db=users_db, tg_id=message.from_user.id)
    if not user.load_from_db():
        user.write_to_db()
    await state.finish()
    await message.answer(StartMenuStrings.HELLO.format(message.from_user.first_name),
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(StartMenuStrings.INFO(), reply_markup=start_menu)


@dp.callback_query_handler(Text(StartMenuStrings.MENU_QUERY), state='*')
async def menu_by_query(call: types.CallbackQuery, state: FSMContext):
    message = call.message
    await state.finish()
    await message.answer(StartMenuStrings.INFO(), reply_markup=start_menu)
    await call.answer()


@dp.message_handler(Text(GettingMessageStrings.STOP_SPAM), state='*')
async def stopping_spam(message: types.Message):
    users_db.update_machine(message.from_user.id, False)
    users_db.update_stop(message.from_user.id, True)


@dp.message_handler(Command(CommandsStrings.GET_ID), state='*')
async def get_id(message: types.Message):
    await message.answer(message.chat.id)
