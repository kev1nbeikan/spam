from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter

from data import ADMINS
from loader import users_db


class IsAdminFilter(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in ADMINS


class IsNotSpammingFilter(BoundFilter):
    async def check(self, message: types.Message):
        return not users_db.get_user_machine_is_spam(message.from_user.id)
