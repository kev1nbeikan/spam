import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from misc.db_api import User
from loader import users_db

class GetDBUser(BaseMiddleware):

    async def on_process_message(self, message: types.Message, data: dict):
        user = User(db=users_db,  tg_id=message.from_user.id)
        logging.info('check...')
        if not user.load_from_db():
            logging.info('added')
            user.write_to_db()