import logging
from datetime import datetime, timedelta

from .spam_memory import MembersDB
from .users import UsersDB


class NeedMembersDB(Exception):
    pass


class User:
    def __init__(self, db: UsersDB, tg_id: int, member_end: int = None, is_spamming: bool = False, c: int = 0,
                 is_stopped: bool = None, msg: str = None, repeat_one_acc: int = None):
        self.tg_id = tg_id
        self.member_end = member_end
        self.db = db
        self.is_spam = is_spamming
        self.members_db: MembersDB = None
        self.count = c
        self.is_stop = is_stopped
        self.msg = msg
        self.repeat_one_acc = repeat_one_acc

    def get_one_db(self):
        return self.db.get_user(user_id=self.tg_id)

    def add_one_db(self, member_end):
        return self.db.add_user(self.tg_id, member_end)

    def update_count(self, c: int):
        return self.db.update_count(self.tg_id, c)

    def update_msg(self, msg: str):
        return self.db.update_msg(self.tg_id, msg)

    def update_repeat(self, count: int):
        return self.db.update_one_acc_repeat(self.tg_id, count)

    def get_msg(self):
        return self.db.get_msg(self.tg_id)

    def get_count(self):
        count = self.db.get_user_cc_spam(self.tg_id)
        return count if count else 0

    def get_repeat(self):
        repeat = self.db.get_user_cc_count_repeat_one_acc(self.tg_id)
        return repeat if repeat else 1

    def get_stop(self):
        return self.db.get_user_stop_state(self.tg_id)

    def get_spam_state(self):
        return self.db.get_user_cc_spam(self.tg_id)

    def update_stop(self):
        self.db.update_stop(self.tg_id, self.is_stop)

    def delete_one_db(self):
        self.db.delete_user(self.tg_id)

    def load_from_db(self):
        if not self.is_exists():
            return False
        self.member_end, self.is_spam, self.count, self.is_stop, self.msg, self.repeat_one_acc = self.get_one_db()

        return True

    def write_to_db(self):
        if self.is_exists():
            if self.member_end is not None:
                self.db.update_membership(self.tg_id, self.member_end)
            if self.is_spam is not None:
                self.db.update_machine(self.tg_id, self.is_spam)
            if self.is_stop is not None:
                self.update_stop()
            if self.msg is not None:
                self.update_msg(self.msg)
            return

        self.add_one_db(self.member_end)

    def update_machine(self):
        if self.is_exists():
            self.db.update_machine(self.tg_id, self.is_spam)
            return

        self.add_one_db(self.member_end)

    def setup_members_db(self, db: MembersDB):
        self.members_db = db

    def get_members(self):
        if self.members_db is None:
            raise NeedMembersDB('Нет БД для спам базы. members_db is None. Используй setup_members_db(members_db)')
        return self.members_db.get_all_members(self.tg_id)

    def add_member(self, member_id):
        self.members_db.add_member(self.tg_id, member_id)

    def delete_member(self, member_id):
        self.members_db.delete_member(self.tg_id, member_id)

    def increase_member(self, days):
        current = datetime.now()
        if self.member_end is not None:
            current = max((current, datetime.fromtimestamp(self.member_end)))

        try:
            new_end = current + timedelta(days=days)
            logging.info(new_end)
        except OverflowError:
            new_end = datetime.now()
        if new_end <= datetime.now():
            self.member_end = None
            return
        else:
            self.member_end = datetime.timestamp(new_end)

    def is_exists(self):
        # logging.info(self.get_one_db())
        res = self.get_one_db()
        return True if res is None or res else False

    def check_m(self):
        if self.member_end is None:
            return False
        if datetime.now() <= datetime.fromtimestamp(self.member_end):
            return True
        self.member_end = None
        return False

    def __str__(self):
        return self.__dict__.__str__()

    def clean_members(self):
        if self.members_db is None:
            raise NeedMembersDB()
        return self.members_db.delete_members_by_id(self.tg_id)

