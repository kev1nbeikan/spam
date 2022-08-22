from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from keyboard import next_step, check_sessions_data, stop_spam
from misc import SpamMachine, get_file_count
from data import DIR_TO_BOTS_FILES, FilesUploadingStrings, GettingMessageStrings
from data import StartMenuStrings, GettingGroupsStrings
from aiogram import types

from misc.db_api import User
from .states import Spam
from loader import admin_bot, dp, users_db


@dp.callback_query_handler(Text(StartMenuStrings.QUERY_SPAM))
async def ask_for_groups(call: types.CallbackQuery, state: FSMContext):
    user = User(db=users_db, tg_id=call.from_user.id)
    if user.get_spam_state():
        await call.message.answer(GettingMessageStrings.SPAM_IS_START, reply_markup=stop_spam)

    await call.message.answer_animation(animation=GettingGroupsStrings.FILE_SERVER_ID_ASK_MESSAGE, caption=GettingGroupsStrings.ASK_MESSAGE, reply_markup=ReplyKeyboardRemove())
    await Spam.first()
    await state.update_data(mashine=set())

    await call.answer()


@dp.message_handler(Text(GettingGroupsStrings.NEXT_STEP), state=Spam.get_group)
async def ask_for_bots(message: types.Message, state: FSMContext):
    await Spam.next()
    user = message.from_user.id
    count = get_file_count(f'{DIR_TO_BOTS_FILES}/{user}/new')
    async with state.proxy() as data:
        members: set = data['mashine']
        if not count:
            await message.answer(GettingGroupsStrings.GET_OR_CHECK_BOTS().format(accs=count, people=len(members)), reply_markup=ReplyKeyboardRemove())
        else:
            inline = InlineKeyboardMarkup().add(
                InlineKeyboardButton(FilesUploadingStrings.CHECK_ACCS,
                                     callback_data=check_sessions_data.new(folder=f'{user}')))
            await message.answer(GettingGroupsStrings.GET_OR_CHECK_BOTS().format(accs=count, people=len(members)), reply_markup=inline)
        await message.answer_photo(caption=FilesUploadingStrings.EXAMPLE_OF_ORDER_ZIP, photo=FilesUploadingStrings.FILE_SERVER_ID_ASK_ZIP)





@dp.message_handler(state=Spam.get_group)
async def download_groups(message: types.Message, state: FSMContext):
    text = message.text
    machine = SpamMachine(bot=admin_bot)
    res = ''
    await message.answer(GettingGroupsStrings.LOAD_DATA)
    pattern = '{} - {}'
    lst = text.split()
    async for ch in machine.get_channels(lst):
        res += pattern.format(ch.name, ch.msg) + '\n'
    if machine.members:
        await message.answer(res, reply_markup=next_step)
    else:
        await message.answer(res)
    async with state.proxy() as data:
        data['mashine'] = data['mashine'].union(machine.members)





