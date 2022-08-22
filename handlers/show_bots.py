import logging

from aiogram import types
from aiogram.dispatcher.filters import Text

from data import StartMenuStrings, ShowBotsStrings, SUCCESS_STRING, DIR_TO_BOTS_FILES, SessionHandleStrings
from keyboard.inline import delete_bots
from loader import dp, sessions_db, file_handler, members_db
from .filters import IsNotSpammingFilter


@dp.callback_query_handler(Text(StartMenuStrings.QUERY_BOT), IsNotSpammingFilter())
async def show_bots(call: types.CallbackQuery):
    work_bot_count = 0
    sessions = sessions_db.get_all_by_dir_through_session_handle(file=call.from_user.id)
    for session in sessions:
        logging.info(session)
        if await session.check_acc():
            work_bot_count += 1

    await call.message.answer(ShowBotsStrings.GET_OR_CHECK_BOTS.format(work=work_bot_count, accs=len(sessions)),
                              reply_markup=delete_bots)


@dp.callback_query_handler(Text(ShowBotsStrings.DELETE_ALL_BOTS_QUERY))
async def delete_all_bots(call: types.CallbackQuery):
    sessions_db.delete_all_from_dir(call.from_user.id)
    file_handler.remove_all_from_dir(f'{DIR_TO_BOTS_FILES}/{call.from_user.id}/new')
    await call.answer(SUCCESS_STRING)
    await show_bots(call)


@dp.callback_query_handler(Text(ShowBotsStrings.DELETE_NOTWORKING_BOTS_QUERY))
async def delete_notworking_bots(call: types.CallbackQuery):
    for session in sessions_db.get_all_by_dir_through_session_handle(call.from_user.id):
        if session.ban_info == SessionHandleStrings.BOT_DONT_WORK:
            session.delete(from_files=True, from_db=True)
    await call.answer(SUCCESS_STRING)
    await show_bots(call)


@dp.callback_query_handler(Text(ShowBotsStrings.DELETE_ALL_MEMBERS_QUERY))
async def delete_all_members(call: types.CallbackQuery):
    members_db.delete_members_by_id(call.from_user.id)
    await call.answer(SUCCESS_STRING)
