import asyncio
import dataclasses
import logging
from random import randint

from aiogram import types
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import ChatAdminRequiredError

from data import GettingGroupsStrings, SessionHandleStrings
from .db_api import Session, BotFileDB, UsersDB, User
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

    async def start_spam(self, msg: str, user_db: UsersDB, user: User, message: types.Message, repeat_one_acc):
        user_id = user.tg_id
        msg = str(msg)
        if self.db is None:
            raise NeedDbError('нет бд')
        bots = self.get_bots()
        # logging.info(self.bots)
        s = bots.__next__()
        user.update_count(0)
        count = 0
        if s is None:
            self._finish_spam(user_db, user_id, user)
            return count
        tg = await s.connect()
        user.is_stop = False
        user.update_stop()
        from_one_acc_sent_count = 0
        for m in self.members:
            user.delete_member(m)
            while True:
                try:
                    if not user_db.get_user_machine_is_spam(user_id):
                        self._finish_spam(user_db, user_id, user)
                        await tg.disconnect()
                        return count
                    # print(user_db.get_user_machine(user_id))
                    logging.info(m)
                    await tg.send_message(message=msg, entity=m)
                    await message.answer(f'Отправлено в {m}')
                    count += 1
                    user.update_count(count)
                    from_one_acc_sent_count += 1
                    await asyncio.sleep(randint(10, 30))
                    if from_one_acc_sent_count == repeat_one_acc:
                        raise Exception('RepeatFromOneAccLimitReached')
                    break
                except Exception as ex:
                    await tg.disconnect()
                    s.err_info = ex.__str__()
                    s.ban_info = SessionHandleStrings.BOT_DONT_WORK

                    if s.err_info == 'The user has been deleted/deactivated (caused by ResolveUsernameRequest)':
                        s.delete(from_files=True, from_db=True)

                    s.write_to_db()
                    s = bots.__next__()
                    logging.info('next_bot')
                    if s is None:
                        self._finish_spam(user_db, user_id, user)
                        return count
                    from_one_acc_sent_count = 0
                    await asyncio.sleep(3)
                    tg = await s.connect()
        self._finish_spam(user_db, user_id, user)
        await tg.disconnect()
        return count

    def _finish_spam(self, user_db, user_id, user):
        user.is_stop = True
        user.is_spam = False
        user.update_stop()
        user.update_machine()

    def get_bots(self):
        if self.db is None:
            raise NeedDbError('нет бд')

        for name, folder in self.bots:
            s = Session(db=self.db, name=name, folder=folder)
            s.load_from_db()
            if not s.is_file_session_exists():
                s.delete(from_db=True)
                continue

            yield s
        yield None


class NeedDbError(Exception):
    pass


class NeedBotError(Exception):
    pass
