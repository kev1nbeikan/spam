from dataclasses import dataclass
ADMIN_CHAT_URL = 'https://t.me/Durovs_Son'

MEMBER_END_WARN = 'Подписка кончилась🕔'

@dataclass
class CommandsStrings:
    START = 'start'
    EXIT = 'exit'
    ADMIN = 'admin'
    GET_ID = 'get_id'
    GIVE = 'give'
    ITEMS = 'items'
    MESSAGES = 'messages'


class CommandsExplainStrings:
    START = 'меню📋'
    EXIT = 'выход'
    GET_ID = 'узнать своей айди👨‍💻'
    ADMIN = 'admin🤚'


@dataclass
class StartMenuStrings:

    QUERY_CURRENT_SPAM = 'cc_spam_info'
    CURRENT_SPAM = 'запущенная рассылка'
    BOT = 'ваши аккаунты'
    QUERY_BOT = 'look_bots'
    QUERY_SPAM = 'spam'
    QUERY_STATUS = 'status'
    QUERY_SUPPORT = ADMIN_CHAT_URL
    HELLO = 'Привет, {}🖐. '
    INFO = f'Это бот🤖 для рассылки рекламы. Покупай <b>подписку</b> и жми <b>рассылка</b>, чтобы прорекламировать свой продукт'

    SPAM = 'Рассылка📨'
    MEMBERSHIP = 'Подписка🕔'
    SUPPORT = 'support🆘'
    MENU_QUERY = 'menu'
    MENU = 'меню'


@dataclass
class GettingGroupsStrings:
    ASK_MESSAGE = 'Отправьте <a href="https://t.me/learn_for_shaida_bot">@имена_групп</a> сообщениями, разделяя пробелами или новой строкой.\n<b>доступны только открытые группы</b>'
    IS_NOT_SUPERGROUP = '❗нет доступа к закрытой🔒 группе'
    NOT_EXIST_GROUP = '❗группы не существует'
    PATTERN_INFO_COUNT = 'получено участников👨‍💻: {count} '
    NEXT_STEP = 'следующий шаг🏃‍♂'
    GET_OR_CHECK_BOTS = 'Вас услышат человек👨‍💻: {people}.\nАккаунтов🤖 для рассылки: {accs}\nВы можете отправить архивом(zip)🗄 новые аккаунты. '
    LOAD_DATA = 'Получение пользователей'
    FILE_SERVER_ID_ASK_MESSAGE = "CgACAgIAAxkBAAIugGLeywvupVGM5GhEIryF_9ctPFUOAAJ-GAACxaPpSgcpLS4aBITNKQQ"
    # FILE_SERVER_ID_ASK_MESSAGE = 'CgACAgIAAxkBAAOWYt1LxOz44Z8_6Whp6lJdSnYRUZgAAosYAALFo-lKSNuz81oZ9RYpBA'




@dataclass
class SessionHandleStrings:
    ASKING_NEW_AUTH = 'Требует новой авторизации'
    BOT_WORK = 'work'
    BOT_DONT_WORK = '-'


@dataclass
class FilesUploadingStrings:
    WRONG_TYPE_FILE = '❗Файл неверного формата (доступны .zip)'
    WRONG_SIZE_FILE = 'Слишком большой размер(<100 МБ)'
    WRONG_CONTENT = '❗Содержимое файла не соответствует шаблону'
    CHECKING_FILES  = 'Разархивация и проверка файла'
    SUCCESS = 'Успешно✅'
    SUCCESS_WITH_ISSUE = 'Успешно✅ загружены файлы, кроме'
    CHECK_ACCS = 'проверить аккаунты🤖'
    CHECKING_BOTS = 'проверка ботов {count}'
    QUERY_CHECK_ACCS = 'check_accs'
    FILE_SERVER_ID_ASK_ZIP = 'AgACAgIAAxkBAAIuimLey2FqGGo9tR_qNxsT0MowHiozAAKewTEbp8iZSrIdc8_0ueeNAQADAgADcwADKQQ'
    # FILE_SERVER_ID_ASK_ZIP = "AgACAgIAAxkBAAOAYt1F9GBHAAFiVwkG6Jan10WCmy_BAALdvTEbxaPpSu6GJFsv1KPKAQADAgADcwADKQQ"
    EXAMPLE_OF_ORDER_ZIP = 'Пример организации файлов📂 в архиве'



@dataclass
class GettingMessageStrings:
    ASK_MESSAGE = 'Введите ваше сообщение для рассылки'
    IS_CORRECT = 'начать рассылку'
    CHANGE = 'изменить'
    IS_CORRECT_QUERY = 'correct'
    CHANGE_QUERY = 'change'
    START_SPAM = 'Рассылка началась...Ожидайте окончания'
    RESULT = 'О вас узнали человек: {count}'
    ASK_PAY_MSG = 'Для того, чтобы продолжить нужно приобрести подписку.'
    STOP_SPAM = 'Остановить спам'



@dataclass
class SelMembershipStrings:
    QUERY_SELL = 'buy_ms'
    QUERY_PAY = 'pay_ms'
    FORMAT_DATE = '%d.%m.%Y: %H-%M'
    STATUS = '''{user}🙍
🕚Подписка: <b>{ms}</b>'''
    NO_MS = 'нет'
    BILL_COMMENT = '''Товар {product}\t
оплата пользователем {name} (tg_id={tg_id})\t
Стоимость {price}\t
+дней {days}\t'''
    CHECK = 'подтвердить💸'
    BILL_MESSAGE = '<b>Перейди по ссылке, чтобы оплатить💸 (❗жми потвердить только после оплаты❗):</b>\n' \
                   '{url}'
    ERROR = f'⚡Ошибка, обратитесь в <a href="{ADMIN_CHAT_URL}">поддержку</a>🆘'
    SUCCESS_BILL = 'Оплата прошла успешно✅'
    NONE_BILL = 'Оплаты не было🚫'


@dataclass
class AdminPanelStrings:
    PANEL = f'/{CommandsStrings.GIVE} изменить подиску юзера\n/{CommandsStrings.ITEMS} продукты\n/{CommandsStrings.MESSAGES} редактировать тект\n/{CommandsStrings.EXIT} выход'

    ASK_ID = 'Введите айди юзера'
    GIVE = 'дать дней'
    TAKE = 'отменить дней'
    ASK_NUM = 'введите число'
    ASK_NAME = 'введите имя'
    ASK_PRICE = 'введите цену'
    ASK_DAYS = 'введите дни'
    ERROR = 'ошибка, неправильный ввод'
    NOT_EXISTS_USER = 'юзер еще не писал боту'
    SHOW_USER = 'статус юзера'
    ADD_MEM = 'добавить подписку'
    STATUS = '''{user}🙍
    🕚Подписка: <b>{ms}</b>'''
    CHANGE_MS_QUERY = 'ch_ms'
    CHANGE_NAME_MS_QUERY = 'name'
    CHANGE_DAYS_MS_QUERY = 'days'
    CHANGE_PRICE_MS_QUERY = 'price'
    CHANGE_DEL_MS_QUERY = 'del'
    SUCCESS = 'успешно'

    CHANGE_MSG_QUERY = 'ch_msg'


@dataclass
class ShowSpamStatusStrings:
    TURN_QUERY = 'turn_spam'
    TURN_OFF = 'остановить'
    TURN_UP = 'запустить'
    UPDATE = 'обновить'
    STOPPING = 'Остановка рассылки'
    WAIT = 'Рассылка еще запущена, но будет остановлена в течение 20 с'
    UPDATE_ASK_QUERY = 'update_and_turn'
    IS_SPAM = 'Состояние: <b>{is_spam}</b>\n'
    INFO = 'Состояние: <b>{is_spam}</b>\n'  \
           'О вас узнало: {count}\n' \
           'Осталось: {remain}'