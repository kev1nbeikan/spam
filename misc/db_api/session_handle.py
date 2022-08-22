import dataclasses
import logging

from telethon import TelegramClient
from telethon.errors import AuthKeyUnregisteredError
from telethon.tl.functions.channels import JoinChannelRequest

from data import DIR_TO_BOTS_FILES
from data import SessionHandleStrings
from misc.filehandlers import LocalFileHandler


class Session:
    def __init__(self, db,
                 name: str = None,
                 folder: str = None,
                 ban_info: str = None,
                 err: str = None,
                 app_version: str = None,
                 device_model: str = None,
                 system_version: str = None,
                 lang_code: str = None,
                 ipv6: bool = None,
                 phone_number: bool = None,
                 app_id: int = None,
                 app_hash: str = None):
        self.name = name
        self.folder = str(folder)
        self.ban_info = ban_info
        self.err_info = err
        self.db = db
        self.path = DIR_TO_BOTS_FILES + '/' + self.folder + '/new/'
        self.path_file = f'{self.path}{self.name}.session'
        self.file_handler = LocalFileHandler()

        self.app_version = app_version
        self.device_model = device_model
        self.system_version = system_version
        self.lang_code = lang_code
        self.ipv6 = ipv6
        self.phone_number = phone_number
        self.app_id = app_id
        self.app_hash = app_hash
        self.CHANNEL_TO_TRY_MESSAGE = '@test_group_for_spam'

    def get_one_db(self, *args, **kwargs):
        return self.db.get_one(self.name, self.folder, *args, **kwargs)

    def add_one_db(self, *args, **kwargs):
        return self.db.add_one(self.name, self.folder, *args, **kwargs)

    def update_ban_one_db(self, *args, **kwargs):
        return self.db.update_ban(name=self.name, folder=self.folder, *args, **kwargs)

    def update_err_one_db(self, *args, **kwargs):
        return self.db.update_error_info(name=self.name, folder=self.folder, *args, **kwargs)

    def load_from_db(self):
        info = self.get_one_db(get_all=True)
        if not info:
            return False
        self.name, self.ban_info, self.folder, self.err_info, \
        self.app_version, self.device_model, self.system_version, \
        self.lang_code, self.ipv6, self.phone_number, self.app_id, self.app_hash = info

        return True

    def write_to_db(self):
        info = self.get_one_db(ban=True, err_info=True)
        if not info:
            self.add_one_db(self.ban_info, self.err_info, self.app_version, self.device_model,
                            self.phone_number, self.ipv6, self.lang_code, self.system_version, self.app_id,
                            self.app_hash)
            return
        ban, err = info
        if ban != self.ban_info:
            self.update_ban_one_db(ban=self.ban_info)

        if err != self.err_info:
            self.update_err_one_db(err=self.err_info)

    def delete_from_db(self):
        self.db.delete_one(self.name, self.folder)

    def delete(self, from_files=False, from_db=True):
        if from_files:
            self.file_handler.remove(self.path_file)
        if from_db:
            self.delete_from_db()

    def is_file_session_exists(self):
        return self.file_handler.exists(self.path_file)

    async def check_acc(self) -> bool:
        """
        Проверяет аккаунт на возможность входа
        :param name: путь до сессии
        :return: bool
        """

        if not (self.app_id and self.app_hash):
            self.err_info = 'Your API ID or Hash cannot be empty or None. Refer to telethon.rtfd.io for more information.'
            self.ban_info = SessionHandleStrings.BOT_DONT_WORK
            return False
        telegram = TelegramClient(self.path + f'/{self.name}', self.app_id, self.app_hash)
        try:
            await telegram.connect()
            await telegram((JoinChannelRequest(channel=self.CHANNEL_TO_TRY_MESSAGE)))
            await telegram.send_message(message='test_message', entity=self.CHANNEL_TO_TRY_MESSAGE)
            await telegram.disconnect()
            self.ban_info = SessionHandleStrings.BOT_WORK
            return True
        except Exception as err:

            if isinstance(err, AuthKeyUnregisteredError):
                self.err_info = SessionHandleStrings.ASKING_NEW_AUTH
            else:
                self.err_info = err.__str__()
            self.ban_info = SessionHandleStrings.BOT_DONT_WORK
            await telegram.disconnect()

            return False

    async def connect(self) -> TelegramClient | bool:
        telegram = TelegramClient(self.path + f'/{self.name}',
                                  api_id=self.app_id,
                                  api_hash=self.app_hash,
                                  app_version=self.app_version,
                                  device_model=self.device_model,
                                  system_version=self.system_version,
                                  lang_code=self.lang_code)
        try:
            await telegram.connect()
            return telegram
        except Exception as ex:
            raise
            return False

    def __str__(self):
        return self.__dict__.__str__()

    __repr__ = __str__

class NoSuchFileError(Exception):
    pass
