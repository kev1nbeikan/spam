from .sessions import DBBaseObject


class UsersDB(DBBaseObject):
    NAME_OF_TABLE = 'users'
    IDENTIFIER_LINE_NAME = 'id'
    MEMBERSHIP_LINE_NAME = 'member_end'
    MACHINE_STATE_LINE_NAME = 'is_spamming'
    COUNT_CURRENT_SPAM = 'current_c_spam'
    IS_STOP_BY_SCRIPT = 'is_stopped'
    MSG = 'message'
    REPEAT_ONE_ACC = 'repeat_one_acc'

    def make_table_users(self):
        users = f'''CREATE TABLE IF NOT EXISTS {self.NAME_OF_TABLE}(
                    {self.IDENTIFIER_LINE_NAME} int NOT NULL,
                    {self.MEMBERSHIP_LINE_NAME} TIMESTAMP,
                    {self.MACHINE_STATE_LINE_NAME} int,
                    {self.COUNT_CURRENT_SPAM} bool,
                    {self.IS_STOP_BY_SCRIPT} bool,
                    {self.MSG} str,
                    {self.REPEAT_ONE_ACC} int);'''
        self.execute(users, commit=True)

    def update_membership(self, user_id: int, sub: int = None):
        """
        :param user_id: id from telegram
        :param sub: datetime.timestamp
        :return:
        """
        command = f'''UPDATE {self.NAME_OF_TABLE} SET {self.MEMBERSHIP_LINE_NAME} = ? WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''
        self.execute(command, (sub, user_id), commit=True)

    def update_machine(self, user_id: int, is_spam: int = 0):

        command = f'''UPDATE {self.NAME_OF_TABLE} SET {self.MACHINE_STATE_LINE_NAME} = ? WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''

        self.execute(command, (is_spam, user_id), commit=True)

    def update_count(self, user_id: int, c: int):
        command = f'''UPDATE {self.NAME_OF_TABLE} SET {self.COUNT_CURRENT_SPAM} = ? WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''

        self.execute(command, (c, user_id), commit=True)

    def update_stop(self, user_id: int, stop: bool):
        command = f'''UPDATE {self.NAME_OF_TABLE} SET {self.IS_STOP_BY_SCRIPT} = ? WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''

        self.execute(command, (stop, user_id), commit=True)

    def update_msg(self, user_id: int, msg: str):
        command = f'''UPDATE {self.NAME_OF_TABLE} SET {self.MSG} = ? WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''

        self.execute(command, (msg, user_id), commit=True)

    def update_one_acc_repeat(self, user_id: int, count: int = 1):
        command = f'''UPDATE {self.NAME_OF_TABLE} SET {self.REPEAT_ONE_ACC} = ? WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''
        self.execute(command, (count, user_id), commit=True)

    def get_msg(self, user_id: int):
        command = f'''SELECT {self.MSG} FROM {self.NAME_OF_TABLE} WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''

        f = self.execute(command, (user_id,), fetch_one=True)
        if f is None:
            return ()
        return f[0]

    def add_user(self, user_id: int, sub: int = None):
        command = f'''INSERT INTO {self.NAME_OF_TABLE}({self.IDENTIFIER_LINE_NAME}, {self.MEMBERSHIP_LINE_NAME}) VALUES(?, ?)'''
        self.execute(command, (user_id, sub), commit=True)

    def get_user(self, user_id: int):
        command = f'''SELECT * FROM {self.NAME_OF_TABLE} WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''
        f = self.execute(command, (user_id,), fetch_one=True)
        if f is None:
            return ()
        return f[1:]

    def get_user_machine_is_spam(self, user_id: int):
        command = f'''SELECT {self.MACHINE_STATE_LINE_NAME} FROM {self.NAME_OF_TABLE} WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''
        f = self.execute(command, (user_id,), fetch_one=True)
        if f is None:
            return ()
        return f[0]

    def get_user_cc_spam(self, user_id: int):
        """
        cc_spma - curent count spam
        :param user_id:
        :return:
        """
        command = f'''SELECT {self.COUNT_CURRENT_SPAM} FROM {self.NAME_OF_TABLE} WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''
        f = self.execute(command, (user_id,), fetch_one=True)
        if f is None:
            return ()
        return f[0]

    def get_user_cc_count_repeat_one_acc(self, user_id: int):
        """
        cc_spma - curent count spam
        :param user_id:
        :return:
        """
        command = f'''SELECT {self.REPEAT_ONE_ACC} FROM {self.NAME_OF_TABLE} WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''
        f = self.execute(command, (user_id,), fetch_one=True)
        if f is None:
            return ()
        return f[0]

    def get_user_stop_state(self, user_id: int):
        """
        cc_spma - curent count spam
        :param user_id:
        :return:
        """
        command = f'''SELECT {self.IS_STOP_BY_SCRIPT} FROM {self.NAME_OF_TABLE} WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''
        f = self.execute(command, (user_id,), fetch_one=True)
        if f is None:
            return ()
        return f[0]

    def get_users(self):
        command = f'''SELECT * FROM {self.NAME_OF_TABLE};'''
        return self.execute(command, fetch_all=True)

    def delete_user(self, user_id: int):
        command = f'DELETE FROM {self.NAME_OF_TABLE} WHERE {self.IDENTIFIER_LINE_NAME} = ?;'
        self.execute(command, (user_id,), commit=True)

    def reset_spam(self):
        command = f'''UPDATE {self.NAME_OF_TABLE} SET {self.IS_STOP_BY_SCRIPT} = 1, {self.MACHINE_STATE_LINE_NAME} = 0;'''
        self.execute(command, commit=True)
