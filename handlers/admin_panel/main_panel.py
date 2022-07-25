from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton

from data import AdminPanelStrings, CommandsStrings
from loader import dp, users_db, products_db, message_db
from handlers.filters import IsAdminFilter
from handlers.states import AdminChangeUser
from misc.db_api import User
from keyboard import add_membership, change_per_of_user, change_msh_data, change_msg_data


@dp.message_handler(IsAdminFilter(), Command(CommandsStrings.ADMIN), state='*')
async def show_admin_menu(message: types.Message, state: FSMContext):
    await state.finish()
    # await dp.bot.set_my_commands(await dp.bot.get_my_commands() + [BotCommand(CommandsStrings.GIVE, 'id')])
    await message.answer(AdminPanelStrings.PANEL)



@dp.message_handler(IsAdminFilter(), Command(CommandsStrings.ITEMS))
async def give(message: types.Message):
    products = products_db.get_products()
    await message.answer(text='тарифы', reply_markup=add_membership)
    for product in products:
        list_m_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        list_m_keyboard.row(
            InlineKeyboardButton('имя', callback_data=change_msh_data.new(cmd=AdminPanelStrings.CHANGE_NAME_MS_QUERY, id_=product.id_)),
            InlineKeyboardButton('дни', callback_data=change_msh_data.new(cmd=AdminPanelStrings.CHANGE_DAYS_MS_QUERY, id_=product.id_)),
            InlineKeyboardButton('цена', callback_data=change_msh_data.new(cmd=AdminPanelStrings.CHANGE_PRICE_MS_QUERY, id_=product.id_)),
            InlineKeyboardButton('удалить', callback_data=change_msh_data.new(cmd=AdminPanelStrings.CHANGE_DEL_MS_QUERY, id_=product.id_))
        )

        await message.answer(text=f'{product.id_}\n<b>имя</b>: {product.name}\n<b>дни</b>: {timedelta(days=product.days).__str__()}\n<b>цена</b>: {product.price}',
                             reply_markup=list_m_keyboard)




@dp.message_handler(IsAdminFilter(), Command(CommandsStrings.MESSAGES))
async def sections(message: types.Message):
    sections =  message_db.get_sections()
    for section in sections:
        list_m_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        list_m_keyboard.row(
            InlineKeyboardButton('изменить', callback_data=change_msg_data.new(section=section.section)),
        )
        await message.answer(text=section.text,
                             reply_markup=list_m_keyboard)




@dp.message_handler(Text(CommandsStrings.EXIT), state='*')
async def exit(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('exit')








