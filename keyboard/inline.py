from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from data import StartMenuStrings, GettingMessageStrings, ShowSpamStatusStrings, ShowBotsStrings

start_menu = InlineKeyboardMarkup()
start_menu.row(InlineKeyboardButton(StartMenuStrings.SPAM, callback_data=StartMenuStrings.QUERY_SPAM),
               InlineKeyboardButton(StartMenuStrings.MEMBERSHIP, callback_data=StartMenuStrings.QUERY_STATUS))
start_menu.row(
    InlineKeyboardButton(StartMenuStrings.CURRENT_SPAM, callback_data=StartMenuStrings.QUERY_CURRENT_SPAM),
    InlineKeyboardButton(StartMenuStrings.BOT, callback_data=StartMenuStrings.QUERY_BOT),
)

start_menu.row(InlineKeyboardButton(StartMenuStrings.SUPPORT, url=StartMenuStrings.QUERY_SUPPORT))

is_correct = InlineKeyboardMarkup()
is_correct.row(InlineKeyboardButton(GettingMessageStrings.IS_CORRECT, callback_data=GettingMessageStrings.IS_CORRECT_QUERY))

start_spam = InlineKeyboardMarkup()
start_spam.row(InlineKeyboardButton(GettingMessageStrings.START_SPAM, callback_data=GettingMessageStrings.IS_CORRECT_QUERY))


delete_bots = InlineKeyboardMarkup()
delete_bots.row(
    InlineKeyboardButton(ShowBotsStrings.DELETE_ALL_BOTS, callback_data=ShowBotsStrings.DELETE_ALL_BOTS_QUERY),
    InlineKeyboardButton(ShowBotsStrings.DELETE_NOTWORKING_BOTS, callback_data=ShowBotsStrings.DELETE_NOTWORKING_BOTS_QUERY),
    InlineKeyboardButton(ShowBotsStrings.DELETE_ALL_MEMBERS, callback_data=ShowBotsStrings.DELETE_ALL_MEMBERS_QUERY),
)
