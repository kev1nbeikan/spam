import logging
from datetime import datetime, timedelta

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from glQiwiApi.qiwi.exceptions import QiwiAPIError

from .spamming import make_spam
from misc.db_api import User, Product
from loader import dp, products_db, users_db, qiwi_p2p_client, sessions_db
from data import StartMenuStrings, SelMembershipStrings, SessionHandleStrings, GettingMessageStrings
from keyboard import buy_membership_data, check_paying_data, stop_spam
from .states import Spam







@dp.callback_query_handler(Text(StartMenuStrings.QUERY_STATUS), state='*')
async def show_products(callback: types.CallbackQuery):
    user = User(db=users_db, tg_id=callback.from_user.id)
    if not user.is_exists():
        user.write_to_db()
    else:
        user.load_from_db()
    list_m_keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    products = products_db.get_products()
    for product in products:
        list_m_keyboard.insert(
            InlineKeyboardButton(product.name, callback_data=buy_membership_data.new(product_id=product.id_)))
    list_m_keyboard.insert(InlineKeyboardButton(StartMenuStrings.MENU, callback_data=StartMenuStrings.MENU_QUERY))
    user.check_m()
    user.write_to_db()
    if user.member_end is not None:
        membership = 'до ' + datetime.fromtimestamp(user.member_end).strftime(SelMembershipStrings.FORMAT_DATE)
    else:
        membership = SelMembershipStrings.NO_MS
    await callback.message.answer(
        text=SelMembershipStrings.STATUS.format(user=callback.from_user.first_name, ms=membership),
        reply_markup=list_m_keyboard)
    await callback.answer()


@dp.callback_query_handler(buy_membership_data.filter(), state='*')
async def buy(call: types.CallbackQuery, callback_data: dict):
    product = products_db.get_product(callback_data['product_id'])
    await making_bill(call, product, call.from_user)
    await call.answer()


async def making_bill(callback: types.CallbackQuery, product: Product, user: types.User):
    expire = datetime.now() + timedelta(minutes=4)
    async with qiwi_p2p_client as w:
        try:
            bill = await w.create_p2p_bill(amount=product.price,
                                           comment=SelMembershipStrings.BILL_COMMENT.format(name=user.first_name,
                                                                                            tg_id=user.id,
                                                                                            product=product.name,
                                                                                            price=product.price,
                                                                                            days=product.days),
                                           expire_at=expire,
                                           pay_source_filter=['qw', 'card', 'mobile'])
            keyboard = InlineKeyboardMarkup(resize_keyboard=True)
            keyboard.row(InlineKeyboardButton(text=SelMembershipStrings.CHECK,
                                              callback_data=check_paying_data.new(bill_id=bill.id, days=product.days)))

            await callback.message.answer(text=SelMembershipStrings.BILL_MESSAGE.format(url=bill.pay_url),
                                          reply_markup=keyboard)
        except QiwiAPIError as err:
            await callback.message.answer(SelMembershipStrings.ERROR + '\n' + err.__str__(), disable_web_page_preview=True)
            raise


@dp.callback_query_handler(check_paying_data.filter(), state='*')
async def confirm(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    days = float(callback_data['days'])
    bill = callback_data['bill_id']
    user = User(db=users_db, tg_id=callback.from_user.id)
    user.load_from_db()
    async with qiwi_p2p_client as w:
        try:
            # if await w.check_if_bill_was_paid(await w.get_bill_by_id(bill)):
                # await callback.answer()
            if True:
                user.increase_member(days)
                logging.info(user.member_end)
                user.write_to_db()
                await callback.message.answer(SelMembershipStrings.SUCCESS_BILL)
                if await state.get_state() == Spam.get_repeat.state:
                    await make_spam(callback, user, state)
            else:
                await callback.message.answer(SelMembershipStrings.NONE_BILL)
                await callback.answer()
        except QiwiAPIError as err:
            await callback.message.answer(SelMembershipStrings.ERROR + '\nerror:' + err.__str__())
            await callback.answer()

