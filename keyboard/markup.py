from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from data import GettingGroupsStrings, AdminPanelStrings, GettingMessageStrings

next_step = ReplyKeyboardMarkup(resize_keyboard=True)
next_step.row(GettingGroupsStrings.NEXT_STEP)
add_membership = ReplyKeyboardMarkup(resize_keyboard=True)
add_membership.row(AdminPanelStrings.ADD_MEM)
change_per_of_user = ReplyKeyboardMarkup(resize_keyboard=True)
change_per_of_user.row(AdminPanelStrings.GIVE, AdminPanelStrings.TAKE)

stop_spam = ReplyKeyboardMarkup(resize_keyboard=True)
stop_spam.row(GettingMessageStrings.STOP_SPAM)