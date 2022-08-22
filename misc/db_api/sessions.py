import sqlite3


class DBBaseObject:
    NAME_OF_TABLE = ''

    def __init__(self, path_db):
        self.path_db = path_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_db)

    def execute(self, command: str, params: tuple = (), fetch_one=False, fetch_all=False, commit=False) -> tuple | list[
        tuple]:

        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(command, params)

        data = None

        if commit:
            connection.commit()
        if fetch_one:
            data = cursor.fetchone()
        if fetch_all:
            data = cursor.fetchall()

        connection.close()

        return data

    def delete(self):
        command = f'''DROP TABLE IF EXISTS {self.NAME_OF_TABLE}'''
        self.execute(command, commit=True)

    def clean(self):
        command = f'''DELETE FROM  {self.NAME_OF_TABLE}'''
        self.execute(command, commit=True)

    def __str__(self):
        return f'<sqlite3DataBaseObject: NAME_OF_TABLE="{self.NAME_OF_TABLE}">'

    __repr__ = __str__


class DBSessions(DBBaseObject):

    def add_sessions(self, dc_id, api_id, test_mode, auth_key, date, user_id, is_bot):
        pass

    def add_version(self, num):
        pass


# класс, который помогает создать ссессию для пайрограма

class PyrogramSessionDB(DBSessions):
    def making_tables(self):
        sessions = '''
        CREATE TABLE IF NOT EXISTS sessions(
        dc_id int PRIMARY KEY,
        api_id int,
        test_mode int,
        auth_key blob,
        date int,
        user_id int,
        is_bot int);
        '''
        self.execute(sessions, commit=True)

        version = '''
        CREATE TABLE IF NOT EXISTS version(number int);'''

        self.execute(version, commit=True)

        peers = '''
        CREATE TABLE IF NOT EXISTS peers(
        id int PRIMARY KEY,
        access_hash int,
        type int,
        username text,
        phone_number text,
        last_update_on int);'''

        self.execute(peers, commit=True)

    def add_sessions(self, dc_id, api_id, test_mode, auth_key, date, user_id, is_bot):
        command = '''INSERT INTO sessions (
                         dc_id,
                         api_id,
                         test_mode,
                         auth_key,
                         date,
                         user_id,
                         is_bot
                     )
                     VALUES (?, ?, ?, ?, ?, ?, ?);'''
        self.execute(command, (dc_id, api_id, test_mode, auth_key, date, user_id, is_bot), commit=True)

    def add_version(self, num):
        command = '''INSERT INTO version (number) VALUES (?);'''
        self.execute(command, (num,), commit=True)


# класс, который помогает достать информацию из сессий, подобных сессиям телетона

class TelethonSessionDB(DBBaseObject):
    # def get_peers(self) -> tuple:
    #     """
    #     get peers
    #     ()
    #     :return: tuple
    #     """
    #     peers = '''SELECT * FROM peers;'''
    #     f = self.execute(peers)
    #     return f

    def get_sessions(self) -> tuple:
        """
        :return: tuple(dc_id, server_address, port, auth_key, takeout_id)
        """
        sessions = '''SELECT * FROM sessions;'''
        f = self.execute(sessions, fetch_all=True)
        return f[0]

    def get_version(self):
        version = '''SELECT * FROM version;'''
        f = self.execute(version, fetch_all=True)
        return f

    def add_in_pyrogram(self, new: PyrogramSessionDB, app_id: int, register_time: int = None):
        session_old = self.get_sessions()
        new.add_sessions(dc_id=session_old[0], api_id=app_id, test_mode=0, auth_key=session_old[3], date=register_time,
                         user_id=None, is_bot=None)
        version_old = self.get_version()[0]
        new.add_version(version_old[0])


# бд, где хранится информация о ботах

class BotFileDB(DBBaseObject):
    NAME_OF_TABLE = 'sessions_check'
    FILE_COLUMN = 'file_name'
    BAN_COLUMN = 'ban_info'
    USER = 'user'
    DIR_INFO = 'dir'
    ERR_COLUMN = 'info'
    APP_COLUMN = 'app_version'
    DEVICE_COLUMN = 'device_model'
    SYSTEM_COLUMN = 'system_version'
    LANG_COLUMN = 'lang_code'
    IPV6_COLUMN = 'ipv6'
    PHONE_COLUMN = 'phone_number'
    APP_ID = 'app_id'
    APP_HASH = 'app_hash'

    from .session_handle import Session
    session_cls = Session

    def make_table_bots(self):
        sessions_check = f'''
                CREATE TABLE IF NOT EXISTS {self.NAME_OF_TABLE}(
                {self.FILE_COLUMN} str,
                {self.BAN_COLUMN} str,
                {self.DIR_INFO} str, 
                {self.ERR_COLUMN} str,
                {self.APP_COLUMN} str,
                {self.DEVICE_COLUMN} str,
                {self.SYSTEM_COLUMN} str,
                {self.LANG_COLUMN} str,
                {self.IPV6_COLUMN} bool,
                {self.PHONE_COLUMN} str,
                {self.APP_ID} int,
                {self.APP_HASH} str);'''
        self.execute(sessions_check, commit=True)

    def _mapping_session_from_db(self, result):
        return self.session_cls(db=self,
                                name=result[0],
                                folder=result[2],
                                ban_info=result[1],
                                err=result[3],
                                app_version=result[4],
                                device_model=result[5],
                                system_version=result[6],
                                lang_code=result[7],
                                ipv6=result[8],
                                phone_number=result[9],
                                app_id=result[10],
                                app_hash=result[11],
                                )

    def get_all(self):
        names = f'''SELECT * FROM {self.NAME_OF_TABLE};'''
        f = self.execute(names, fetch_all=True)
        return f

    def get_all_by_dir_through_session_handle(self, file: str):
        names = f'''SELECT * FROM {self.NAME_OF_TABLE} WHERE {self.DIR_INFO} = ?;'''
        f = self.execute(names, (file,), fetch_all=True)
        return list(map(self._mapping_session_from_db, f)) if f else []

    def get_all_by_dir(self, file: str):
        names = f'''SELECT {self.FILE_COLUMN}, {self.DIR_INFO} FROM {self.NAME_OF_TABLE} WHERE {self.DIR_INFO} = ?;'''
        f = self.execute(names, (file,), fetch_all=True)
        return set(f)


    def get_all_by_ban(self, ban, folder):
        names = f'''SELECT {self.FILE_COLUMN}, {self.DIR_INFO} FROM {self.NAME_OF_TABLE} WHERE {self.BAN_COLUMN} = ? AND {self.DIR_INFO} = ?;'''
        f = self.execute(names, (ban, folder), fetch_all=True)
        return set(f)

    def get_one(self, name: str, folder: str, ban: bool = False, err_info: bool = False, get_all: bool = False):
        names = f'''SELECT {{}} FROM {self.NAME_OF_TABLE} WHERE {self.FILE_COLUMN} = ? and {self.DIR_INFO} = ?;'''
        text = []
        if get_all:
            f = self.execute(names.format('*'), (name, folder), fetch_one=True)
            if f is None:
                return ()
            return f
        if ban:
            text.append(self.BAN_COLUMN)
        if err_info:
            text.append(self.ERR_COLUMN)
        if not text:
            return ()
        f = self.execute(names.format(', '.join(text)), (name, folder), fetch_one=True)
        if f is None:
            return ()
        return f

    def get_one_through_session_handle(self, name: str, folder: str, ban: bool = False, err_info: bool = False,
                                       get_all: bool = False):
        """
        Получает из бд сессию, только сразу классом Session
        :param name:
        :param folder:
        :param ban:
        :param err_info:
        :param get_all:
        :return:
        """
        names = f'''SELECT {{}} FROM {self.NAME_OF_TABLE} WHERE {self.FILE_COLUMN} = ? and {self.DIR_INFO} = ?;'''
        text = []
        if get_all:
            f = self.execute(names.format('*'), (name, folder), fetch_one=True)
            if f is None:
                return ()
            return self._mapping_session_from_db(f)
        if ban:
            text.append(self.BAN_COLUMN)
        if err_info:
            text.append(self.ERR_COLUMN)
        if not text:
            return ()
        f = self.execute(names.format(', '.join(text)), (name, folder), fetch_one=True)
        if f is None:
            return ()
        return self._mapping_session_from_db(f)

    def add_one(self, name: str, folder: str = None, ban: str = None, err: str = None, app: str = None,
                device: str = None, phone: str = None, ipv6: str = None, lang: str = None,
                system: str = None, app_id: int = None, app_hash: str = None):

        command = f'''INSERT INTO {self.NAME_OF_TABLE} (
                {self.FILE_COLUMN},
                {self.BAN_COLUMN},
                {self.DIR_INFO},
                {self.ERR_COLUMN},
                {self.APP_COLUMN},
                {self.DEVICE_COLUMN},
                {self.SYSTEM_COLUMN},
                {self.LANG_COLUMN},
                {self.IPV6_COLUMN},
                {self.PHONE_COLUMN},
                {self.APP_ID},
                {self.APP_HASH}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''

        self.execute(command, (name, ban, folder, err, app, device, system, lang, ipv6, phone, app_id, app_hash),
                     commit=True)

    def delete_one(self, name: str, folder: str):
        command = f'DELETE FROM {self.NAME_OF_TABLE} WHERE {self.FILE_COLUMN} = ? and {self.DIR_INFO} = ?;'
        self.execute(command, (name, folder), commit=True)

    def delete_all_from_dir(self, folder: str):
        command = f'DELETE FROM {self.NAME_OF_TABLE} WHERE {self.FILE_COLUMN} = ?;'
        self.execute(command, (folder, ), commit=True)

    def delete_all_from_dir_by_ban(self, folder: str, ban: str):
        command = f'DELETE FROM {self.NAME_OF_TABLE} WHERE {self.FILE_COLUMN} = ? AND {self.BAN_COLUMN} = ?;'
        self.execute(command, (folder, ban), commit=True)

    def update_ban(self, name: str, folder: str, ban: str = None):
        command = f'''UPDATE {self.NAME_OF_TABLE} SET {self.BAN_COLUMN} = ? WHERE {self.FILE_COLUMN} = ? and {self.DIR_INFO} = ?;'''
        self.execute(command, (ban, name, folder), commit=True)

    def update_error_info(self, name: str, folder: str, err: str = None):
        command = f'''UPDATE {self.NAME_OF_TABLE} SET {self.ERR_COLUMN} = ? WHERE {self.FILE_COLUMN} = ? and {self.DIR_INFO} = ?;'''
        self.execute(command, (err, name, folder), commit=True)


if __name__ == '__main__':
    db = BotFileDB('../../db/main.db')
