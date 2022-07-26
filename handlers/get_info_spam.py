import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageNotModified

from loader import dp, users_db, members_db
from data import StartMenuStrings, ShowSpamStatusStrings, GettingMessageStrings
from misc.db_api import User
from .spamming import make_spam, make_spam_by_db


@dp.callback_query_handler(Text(StartMenuStrings.QUERY_CURRENT_SPAM))
async def show_info(call: types.CallbackQuery):
    user = User(tg_id=call.from_user.id, db=users_db)
    user.load_from_db()
    user.setup_members_db(members_db)
    count = user.get_count()
    remain = set(user.get_members())
    update_and_turn = InlineKeyboardMarkup()
    update_and_turn.row(
        InlineKeyboardButton(ShowSpamStatusStrings.UPDATE, callback_data=ShowSpamStatusStrings.UPDATE_ASK_QUERY))
    update_and_turn.row(
        InlineKeyboardButton(ShowSpamStatusStrings.TURN_OFF if user.is_spam else ShowSpamStatusStrings.TURN_UP,
                             callback_data=ShowSpamStatusStrings.TURN_QUERY))

    await call.message.answer(ShowSpamStatusStrings.INFO.format(count=count,
                                                                remain=len(remain),
                                                                is_spam='work' if user.is_spam else 'stopped'),
                              reply_markup=update_and_turn)

    await call.answer()


@dp.callback_query_handler(Text(ShowSpamStatusStrings.UPDATE_ASK_QUERY))
async def update_info(call: types.CallbackQuery):
    message = call.message
    user = User(tg_id=call.from_user.id, db=users_db)
    user.load_from_db()
    user.setup_members_db(members_db)
    count = user.get_count()

    remain = set(user.get_members())
    try:
        update_and_turn = InlineKeyboardMarkup()
        update_and_turn.row(
            InlineKeyboardButton(ShowSpamStatusStrings.UPDATE, callback_data=ShowSpamStatusStrings.UPDATE_ASK_QUERY))
        update_and_turn.row(
            InlineKeyboardButton(ShowSpamStatusStrings.TURN_OFF if user.is_spam else ShowSpamStatusStrings.TURN_UP, callback_data=ShowSpamStatusStrings.TURN_QUERY))

        await message.edit_text(ShowSpamStatusStrings.INFO.format(count=count,
                                                                  is_spam='work' if user.is_spam else 'stopped',
                                                                  remain=len(remain)), reply_markup=update_and_turn)
    except MessageNotModified:
        pass

    await call.answer()



@dp.callback_query_handler(Text( ShowSpamStatusStrings.TURN_QUERY ))
async def stop_spam(call: types.CallbackQuery, state: FSMContext):
    user = User(tg_id=call.from_user.id, db=users_db)
    user.load_from_db()
    if not user.is_spam and not user.is_stop and user.is_stop is not None:
        await call.message.answer(ShowSpamStatusStrings.WAIT)
        await call.answer()
        return

    user.is_spam = not user.is_spam
    user.update_machine()

    user.load_from_db()
    user.setup_members_db(members_db)
    count = user.get_count()
    remain = set(user.get_members())
    if user.check_m():
        await call.message.answer(GettingMessageStrings.ASK_PAY_MSG)
        return
    try:
        update_and_turn = InlineKeyboardMarkup()
        update_and_turn.row(
            InlineKeyboardButton(ShowSpamStatusStrings.UPDATE, callback_data=ShowSpamStatusStrings.UPDATE_ASK_QUERY))
        update_and_turn.row(
            InlineKeyboardButton(ShowSpamStatusStrings.TURN_OFF if not user.is_stop else ShowSpamStatusStrings.TURN_UP,
                                 callback_data=ShowSpamStatusStrings.TURN_QUERY))

        await call.message.edit_text(ShowSpamStatusStrings.INFO.format(count=count,
                                                                  is_spam='work' if not user.is_stop else 'stopped',
                                                                  remain=len(remain)), reply_markup=update_and_turn)
    except MessageNotModified:
        pass
    if user.is_spam:
        await make_spam_by_db(call, user, state)


