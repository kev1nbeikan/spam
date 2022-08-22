import asyncio

from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand
from aiogram.utils import executor

from data import CommandsStrings, CommandsExplainStrings, MEMBER_END_WARN, ADMINS, AdminPanelStrings, SessionHandleStrings
from loader import admin_bot, users_db, sessions_db
from middlewares import setup
from misc.db_api import User


async def check_membership():
    while True:
        try:
            for user in users_db.get_users():
                print(user)
                user = User(users_db, *user)
                user.load_from_db()
                was_end = user.member_end
                user.check_m()
                if user.member_end is None and was_end is not None:
                    user.db.update_membership(user.tg_id, None)
                    await dp.bot.send_message(user.tg_id, MEMBER_END_WARN)
                await asyncio.sleep(3)
        except:
            raise
        await asyncio.sleep(60)


async def start_up(dp: Dispatcher):
    setup(dp)
    asyncio.create_task(check_membership())
    await dp.bot.set_my_commands([BotCommand(CommandsStrings.START, CommandsExplainStrings.START),
                                  BotCommand(CommandsStrings.GET_ID, CommandsExplainStrings.GET_ID),
                                  BotCommand(CommandsStrings.ADMIN, CommandsExplainStrings.ADMIN)])

    await admin_bot.connect()
    if not await admin_bot.is_user_authorized():
        for admin in ADMINS:
            await dp.bot.send_message(admin, AdminPanelStrings.AUTH_REQUIRE)


async def main():
    for session in sessions_db.get_all_by_dir_through_session_handle(559268824):
        print(await session.check_acc())
        print(session.write_to_db())


if __name__ == '__main__':
    from handlers import dp

    # await admin_bot.start()

    # asyncio.run(main())
    executor.start_polling(dp, on_startup=start_up)
