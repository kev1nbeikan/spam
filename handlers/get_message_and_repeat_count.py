import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import GettingMessageStrings, INCORRECT_INPUT
from keyboard import is_correct, buy_membership_data, suggestions, start_spam
from loader import dp, users_db, products_db
from misc.db_api import User
from .spamming import make_spam
from .states import Spam


@dp.message_handler(state=Spam.get_message)
async def get_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = message.text
    logging.info(await state.get_data())
    await message.answer(message.text, reply_markup=is_correct)


@dp.callback_query_handler(Text(GettingMessageStrings.IS_CORRECT_QUERY), state=Spam.get_message)
async def ask_repeat_count(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(GettingMessageStrings.ASK_REPEAT_FROM_ONE_ACC, reply_markup=suggestions)
    await Spam.get_repeat.set()
    logging.info(await state.get_data())
    await call.answer()


@dp.message_handler(state=Spam.get_repeat)
async def get_repeat_count(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(INCORRECT_INPUT)
    else:
        await message.answer(message.text, reply_markup=start_spam)
        await state.update_data(repeat=int(message.text))
        logging.info(await state.get_data())


@dp.callback_query_handler(Text(GettingMessageStrings.IS_CORRECT_QUERY), state=Spam.get_repeat)
async def start_spam_handler(call: types.CallbackQuery, state: FSMContext):
    user = User(db=users_db, tg_id=call.from_user.id)
    if not user.load_from_db():
        user.write_to_db()

    user.check_m()
    user.write_to_db()
    if user.member_end is None:
        list_m_keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
        products = products_db.get_products()
        for product in products:
            list_m_keyboard.insert(
                InlineKeyboardButton(product.name, callback_data=buy_membership_data.new(product_id=product.id_)))

        await call.message.answer(GettingMessageStrings.ASK_PAY_MSG, reply_markup=list_m_keyboard)
        await call.answer()

        return
    logging.info(await state.get_data())
    await make_spam(call, user, state)
