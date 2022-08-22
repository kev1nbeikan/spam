from aiogram.dispatcher.filters.state import State, StatesGroup


class Spam(StatesGroup):
    get_group = State()
    get_bot_files = State()
    get_message = State()
    get_repeat = State()
    wait_spam = State()


class AdminChangeUser(StatesGroup):
    get_user_id = State()
    panel_of_user = State()
    choose_days = State()


class AdminNewProduct(StatesGroup):
    wait_name = State()
    wait_days = State()
    wait_price = State()


class AdminChangeProduct(StatesGroup):
    wait_name = State()
    wait_days = State()
    wait_price = State()


class AdminChangeMessage(StatesGroup):
    wait_text = State()


class AuthAdminBotStates(StatesGroup):
    wait_code = State()
    wait_password = State()

# +79090874142
