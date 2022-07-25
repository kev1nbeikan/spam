# изменить подписку юзера
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from data import CommandsStrings, AdminPanelStrings, SelMembershipStrings
from handlers.filters import IsAdminFilter
from handlers.states import AdminChangeUser
from keyboard import change_per_of_user
from loader import dp, users_db
from misc.db_api import User


async def show_status(user: User, message: types.Message):
    if user.member_end is not None:
        membership = 'до ' + datetime.fromtimestamp(user.member_end).strftime(SelMembershipStrings.FORMAT_DATE)
    else:
        membership = SelMembershipStrings.NO_MS
    await message.answer(SelMembershipStrings.STATUS.format(user=user.tg_id, ms=membership),
                         reply_markup=change_per_of_user)


@dp.message_handler(IsAdminFilter(), Command(CommandsStrings.GIVE), state='*')
async def give(message: types.Message):
    await message.answer(AdminPanelStrings.ASK_ID)
    await AdminChangeUser.get_user_id.set()



# ввод айди юзера
@dp.message_handler(IsAdminFilter(), state=AdminChangeUser.get_user_id)
async def get_user_id(message: types.Message, state: FSMContext):
    text = message.text
    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer(AdminPanelStrings.ERROR)
        return

    user = User(db=users_db, tg_id=user_id)
    if not user.load_from_db():
        await message.answer(AdminPanelStrings.NOT_EXISTS_USER)
        return
    await show_status(user, message)
    await state.update_data(tg_id=user_id)
    await AdminChangeUser.panel_of_user.set()


@dp.message_handler(IsAdminFilter(), Text(AdminPanelStrings.GIVE), state=AdminChangeUser.panel_of_user)
async def ask_plus_num(message: types.Message, state: FSMContext):
    await message.answer(AdminPanelStrings.ASK_NUM)
    await state.update_data(give=True)
    await AdminChangeUser.choose_days.set()


@dp.message_handler(IsAdminFilter(), Text(AdminPanelStrings.TAKE), state=AdminChangeUser.panel_of_user)
async def ask_minus_num(message: types.Message, state: FSMContext):
    await message.answer(AdminPanelStrings.ASK_NUM)
    await state.update_data(give=False)
    await AdminChangeUser.choose_days.set()



# даем юзеру дни подписки
@dp.message_handler(IsAdminFilter(), state=AdminChangeUser.choose_days)
async def check_num(message: types.Message, state: FSMContext):
    text = message.text
    try:
        days = float(message.text)
        async with state.proxy() as data:
            user = User(db=users_db, tg_id=data['tg_id'])
            give = data['give']
        user.load_from_db()
        if give:
            user.increase_member(+days)
        else:
            user.increase_member(-days)
        await AdminChangeUser.panel_of_user.set()
        user.write_to_db()
        await show_status(user, message)
    except ValueError:
        await message.answer(AdminPanelStrings.ERROR)
        return