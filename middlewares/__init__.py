from aiogram import Dispatcher
from .add_to_db import GetDBUser
from .throttling import ThrottlingMiddleware

def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware(limit=0.5))
