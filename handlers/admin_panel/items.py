import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.filters import IsAdminFilter
from loader import dp
from keyboard import change_msh_data
from data import AdminPanelStrings as astr
from handlers.states import AdminNewProduct, AdminChangeProduct
from loader import products_db
from misc.db_api import Product



@dp.callback_query_handler(IsAdminFilter(), change_msh_data.filter())
async def ch_product_name(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(id_=callback_data['id_'])
    match callback_data['cmd']:
        case astr.CHANGE_DAYS_MS_QUERY:
            await call.message.answer(astr.ASK_DAYS)
            await AdminChangeProduct.wait_days.set()

        case astr.CHANGE_NAME_MS_QUERY:
            await call.message.answer(astr.ASK_NAME)
            await AdminChangeProduct.wait_name.set()


        case astr.CHANGE_PRICE_MS_QUERY:
            await call.message.answer(astr.ASK_PRICE)
            await AdminChangeProduct.wait_price.set()

        case astr.CHANGE_DEL_MS_QUERY:
            products_db.delete_product(callback_data['id_'])



    await call.answer()


@dp.message_handler(IsAdminFilter(), Text(astr.ADD_MEM))
async def add_product(message: types.Message):
    await message.answer(astr.ASK_NAME)
    await AdminNewProduct.wait_name.set()


@dp.message_handler(IsAdminFilter(), state=AdminNewProduct.wait_name)
async def add_product_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(astr.ASK_PRICE)
    await AdminNewProduct.wait_price.set()


@dp.message_handler(IsAdminFilter(), state=AdminNewProduct.wait_price)
async def add_product_price(message: types.Message, state: FSMContext):
    text = message.text
    try:
        price = int(text)
        await state.update_data(price=price)
    except ValueError:
        await message.answer(astr.ERROR + ' ' + astr.ASK_PRICE)
        return
    await message.answer(astr.ASK_DAYS)
    await AdminNewProduct.wait_days.set()


@dp.message_handler(IsAdminFilter(), state=AdminNewProduct.wait_days)
async def add_product_days(message: types.Message, state: FSMContext):
    text = message.text
    logging.info('')
    try:
        days = float(text)
    except ValueError:
        await message.answer(astr.ERROR + ' ' + astr.ASK_DAYS)
        return
    async with state.proxy() as data:
        products_db.add_product(name=data['name'],
                          days=days,
                          price=data['price'])

    await state.finish()



@dp.message_handler(IsAdminFilter(), state=AdminChangeProduct.wait_name)
async def change_product_(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        id_ = data['id_']
    products_db.update_product(indentifier=id_, name=message.text)
    await message.answer(astr.SUCCESS)
    await state.finish()

@dp.message_handler(IsAdminFilter(), state=AdminChangeProduct.wait_days)
async def change_product_days(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            id_ = data['id_']
        products_db.update_product(indentifier=id_, days=float(message.text))
        await message.answer(astr.SUCCESS)
        await state.finish()
    except ValueError:
        await message.answer(astr.ERROR + ' ' + astr.ASK_DAYS)
        return


@dp.message_handler(IsAdminFilter(), state=AdminChangeProduct.wait_price)
async def change_product_price(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            id_ = data['id_']
        products_db.update_product(indentifier=id_, price=int(message.text))
        await message.answer(astr.SUCCESS)
        await state.finish()
    except ValueError:
        await message.answer(astr.ERROR + ' ' + astr.ASK_PRICE)
        return

