import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from data import GettingMessageStrings, SessionHandleStrings
from loader import dp, sessions_db, users_db, products_db
from misc.db_api import User
from .spamming import make_spam
from .states import Spam
from keyboard import is_correct, buy_membership_data, stop_spam
from misc import SpamMachine

@dp.message_handler(state=Spam.get_message)
async def get_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = message.text

    await message.answer(message.text, reply_markup=is_correct)


@dp.callback_query_handler(Text(GettingMessageStrings.IS_CORRECT_QUERY), state=Spam.get_message)
async def start_spam(call: types.CallbackQuery, state: FSMContext):
    # проверка подписки
    user = User(db=users_db, tg_id=call.from_user.id)
    if not user.load_from_db():
        user.write_to_db()

    user.check_m()
    logging.info(user.member_end)
    user.write_to_db()
    logging.info(user.member_end)
    if user.member_end is None:
        list_m_keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
        products = products_db.get_products()
        for product in products:
            list_m_keyboard.insert(
                InlineKeyboardButton(product.name, callback_data=buy_membership_data.new(product_id=product.id_)))

        await call.message.answer(GettingMessageStrings.ASK_PAY_MSG, reply_markup=list_m_keyboard)
        await call.answer()

        return


    await make_spam(call, user, state)


