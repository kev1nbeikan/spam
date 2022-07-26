import asyncio
import dataclasses
import logging

from aiogram import types
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import ChatAdminRequiredError
from data import GettingGroupsStrings, SessionHandleStrings
from .db_api import Session, BotFileDB, UsersDB, User
from random import randint

from .db_api.session_handle import NoSuchFileError


@dataclasses.dataclass
class ChatCheck:
    name: str
    msg: str = None


class SpamMachine():
    def __init__(self, bot: TelegramClient = None):
        self.bot = bot
        self.accs = set()
        self.channels = set()
        self.members = set()
        self.bots = set()
        self.db = None

    async def get_channels(self, channels: list | set):
        if self.bot is None:
            raise NeedBotError('нет бота')
        for ch in channels:
            try:
                count = 0
                for member in await self.bot.get_participants(ch):
                    user = member.username
                    if user is not None:
                        self.members.add(user)
                        count += 1
                yield ChatCheck(name=ch, msg=GettingGroupsStrings.PATTERN_INFO_COUNT.format(count=count))

            except Exception as ex:
                # raise
                if isinstance(ex, ChatAdminRequiredError):
                    yield ChatCheck(name=ch, msg=GettingGroupsStrings.NOT_EXIST_GROUP)
                elif isinstance(ex, ValueError):
                    yield ChatCheck(name=ch, msg=GettingGroupsStrings.NOT_EXIST_GROUP)
                else:
                    yield ChatCheck(name=ch, msg=ex.__str__())

    def load_users(self, users: set):
        self.members = users

    def load_bots(self, bots: set[tuple[str, str]]):
        self.bots = bots


    def set_db(self, db: BotFileDB):
        self.db = db

    async def start_spam(self, msg: str, user_db:UsersDB, user: User):
        user_id = user.tg_id
        if self.db is None:
            raise NeedDbError('нет бд')
        bots = self.get_bots()
        # logging.info(self.bots)
        s = bots.__next__()
        user.update_count(0)
        count = 0
        if s is None:
            user.is_stop = True
            user.update_stop()
            return count
        tg = await s.connect()
        user.is_stop = False
        user.update_stop()
        for m in self.members:
            while True:
                try:
                    if not user_db.get_user_machine(user_id):
                        return count
                    # print(user_db.get_user_machine(user_id))
                    await tg.send_message(message=msg, entity=m)
                    user.delete_member(m)
                    await asyncio.sleep(randint(10, 30))
                    count += 1
                    user.update_count(count)
                    break
                except Exception as ex:
                    # raise
                    await tg.disconnect()
                    s.err_info = ex.__str__()
                    s.ban_info = SessionHandleStrings.BOT_DONT_WORK

                    if s.err_info == 'The user has been deleted/deactivated (caused by ResolveUsernameRequest)':
                        s.delete()

                    s.write_to_db()
                    s = bots.__next__()
                    # logging.info('next_bot')
                    if s is None:
                        user_db.update_machine(user_id, False)
                        user.is_stop = True
                        user.update_stop()
                        return count
                    await asyncio.sleep(3)
                    tg = await s.connect()
        user.is_stop = True
        user.update_stop()
        user_db.update_machine(user_id, False)
        await tg.disconnect()
        return count

    def get_bots(self):
        if self.db is None:
            raise NeedDbError('нет бд')

        for name, folder in self.bots:
            try:
                s = Session(db=self.db, name=name, folder=folder)
                s.load_from_db()
                logging.info(name)
            except NoSuchFileError as ex:
                logging.info(ex.__str__())
                continue
            yield s
        yield None



class NeedDbError(Exception):
    pass


class NeedBotError(Exception):
    pass