from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from data import StartMenuStrings, GettingMessageStrings

start_menu = InlineKeyboardMarkup()
start_menu.row(InlineKeyboardButton(StartMenuStrings.SPAM, callback_data=StartMenuStrings.QUERY_SPAM),
               InlineKeyboardButton(StartMenuStrings.MEMBERSHIP, callback_data=StartMenuStrings.QUERY_STATUS))
start_menu.row(InlineKeyboardButton(StartMenuStrings.SUPPORT, url=StartMenuStrings.QUERY_SUPPORT))

is_correct = InlineKeyboardMarkup()
is_correct.row(InlineKeyboardButton(GettingMessageStrings.IS_CORRECT, callback_data=GettingMessageStrings.IS_CORRECT_QUERY))
