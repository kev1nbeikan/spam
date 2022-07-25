import logging
from datetime import datetime, timedelta

from .users import UsersDB
from .spam_memory import MembersDB


class NeedMembersDB(Exception):
    pass



class User:
    def __init__(self, db: UsersDB, tg_id: int, member_end: int = None, is_spamming: bool= False, c: int = 0):
        self.tg_id = tg_id
        self.member_end = member_end
        self.db = db
        self.is_spam = is_spamming
        self.members_db: MembersDB = None
        self.count = c

    def get_one_db(self):
        return self.db.get_user(user_id=self.tg_id)

    def add_one_db(self, member_end):
        return self.db.add_user(self.tg_id, member_end)

    def update_count(self, c: int):
        return self.db.update_count(self.tg_id, c)

    def get_count(self):
        return self.db.get_user_cc_spam(self.tg_id)

    def delete_one_db(self):
        self.db.delete_user(self.tg_id)

    def load_from_db(self):
        if not self.is_exists():
            return False
        self.member_end, self.is_spam, self.count = self.get_one_db()

        return True

    def write_to_db(self):
        if self.is_exists():
            if self.member_end is not None:
                self.db.update_membership(self.tg_id, self.member_end)
            if self.is_spam is not None:
                self.db.update_machine(self.tg_id, self.is_spam)


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
            raise NeedMembersDB('Нет БД для спам базы members_db is None. Используй setup_members_db(db)')
        return map(lambda x: x[0], self.members_db.get_all_members(self.tg_id))

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
        logging.info(self.member_end)
        if self.member_end is None:
            return False
        if datetime.now() <= datetime.fromtimestamp(self.member_end):
            return True
        self.member_end = None
        logging.info(self.member_end)
        return False

    def __str__(self):
        return self.__dict__.__str__()




