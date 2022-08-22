import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from data import SessionHandleStrings, GettingMessageStrings
from handlers.states import Spam
from keyboard import stop_spam
from loader import sessions_db, users_db, members_db
from misc import SpamMachine
from misc.db_api import User


async def make_spam(call: types.CallbackQuery, user: User, state: FSMContext):
    logging.info(await state.get_data())

    async with state.proxy() as data:
        members = data.get('mashine')
        msg = data.get('msg')
        repeat = data.get('repeat')
    mashine = SpamMachine()
    logging.info(members)
    mashine.set_db(sessions_db)
    mashine.load_users(members)
    user.setup_members_db(members_db)
    user.clean_members()
    for member in members:
        user.add_member(member)
    user.update_msg(msg)
    user.update_repeat(repeat)
    mashine.load_bots(sessions_db.get_all_by_dir(user.tg_id))
    await call.answer()
    await call.message.answer(GettingMessageStrings.SPAM_IS_START, reply_markup=stop_spam)
    await Spam.wait_spam.set()
    user.is_spam = True
    user.write_to_db()
    result = await mashine.start_spam(msg=msg, user=user, user_db=users_db, repeat_one_acc=repeat, message=call.message)
    await call.message.answer(GettingMessageStrings.RESULT.format(count=result), reply_markup=ReplyKeyboardRemove())
    await state.finish()



async def make_spam_by_db(call: types.CallbackQuery, user: User, state: FSMContext):
    members = members_db.get_all_members(user.tg_id)
    msg = user.get_msg()
    repeat = user.get_repeat()
    mashine = SpamMachine()
    mashine.set_db(sessions_db)
    mashine.load_users(members)
    user.setup_members_db(members_db)
    mashine.load_bots(sessions_db.get_all_by_dir(user.tg_id))
    await call.answer()
    await call.message.answer(GettingMessageStrings.SPAM_IS_START, reply_markup=stop_spam)
    await Spam.wait_spam.set()
    user.is_spam = True
    user.write_to_db()
    result = await mashine.start_spam(msg=msg, user=user, user_db=users_db, repeat_one_acc=repeat, message=call.message)
    await call.message.answer(GettingMessageStrings.RESULT.format(count=result), reply_markup=ReplyKeyboardRemove())
    await state.finish()