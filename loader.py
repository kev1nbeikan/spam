import asyncio

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon import TelegramClient
from data import MAIN_DB_NAME, config, APP_ID, APP_HASH, QIWI_TOKEN
from data import StartMenuStrings, GettingGroupsStrings
from misc.db_api import BotFileDB, UsersDB, ShopDB, MessagesDB, MembersDB
from glQiwiApi import QiwiP2PClient
import logging

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,
                    )


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

admin_bot = TelegramClient('new', APP_ID, APP_HASH)
qiwi_p2p_client = QiwiP2PClient(secret_p2p=QIWI_TOKEN)

sessions_db = BotFileDB(MAIN_DB_NAME)
users_db = UsersDB(MAIN_DB_NAME)
products_db = ShopDB(MAIN_DB_NAME)
message_db = MessagesDB(MAIN_DB_NAME)
members_db = MembersDB(MAIN_DB_NAME)

message_db.making_messages_table()

message_db.add_section('bots', GettingGroupsStrings.GET_OR_CHECK_BOTS, requires='{people} {accs}')
message_db.add_section('info', StartMenuStrings.INFO)
StartMenuStrings.INFO = lambda: message_db.get_section('info').text
GettingGroupsStrings.GET_OR_CHECK_BOTS = lambda: message_db.get_section('bots').text

products_db.making_table_shop()
users_db.delete()
users_db.make_table_users()

members_db.making_members_table()
# sessions_db.delete()
sessions_db.make_table_bots()
