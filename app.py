import asyncio
import logging

from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand

from data import CommandsStrings, CommandsExplainStrings, MEMBER_END_WARN
from loader import admin_bot, users_db
from misc.db_api import User
from middlewares import setup
from threading import Thread


async def check_membership():
    while True:
        try:
            for user in users_db.get_users():
                user = User(users_db, *user)
                user.load_from_db()
                was_end = user.member_end
                user.check_m()
                if user.member_end is None and was_end is not None:
                    user.db.update_membership(user.tg_id, None)
                    await dp.bot.send_message(user.tg_id, MEMBER_END_WARN)
                await asyncio.sleep(1)
        except:
            continue
        await asyncio.sleep(60)







async def start_up(dp: Dispatcher):
    setup(dp)
    asyncio.create_task(check_membership())
    await dp.bot.set_my_commands([BotCommand(CommandsStrings.START, CommandsExplainStrings.START),
                                  BotCommand(CommandsStrings.GET_ID, CommandsExplainStrings.GET_ID),
                                  BotCommand(CommandsStrings.ADMIN, CommandsExplainStrings.ADMIN)])

    await admin_bot.connect()

if __name__ == '__main__':
    # asyncio.run(main())
    # from loader import users_db, members_db
    # from misc.db_api import User

    from aiogram import executor, Dispatcher
    from handlers import dp
    executor.start_polling(dp, skip_updates=True, on_startup=start_up)
    # print(sessions_db.get_all_by_ban(SessionHandleStrings.BOT_WORK))
    pass
