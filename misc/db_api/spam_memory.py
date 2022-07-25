import dataclasses
from .sessions import DBBaseObject
from .users import UsersDB

class MembersDB(DBBaseObject):
    NAME_OF_TABLE = 'members'
    IDENTIFIER_LINE_NAME = 'id'
    IDENTIFIER_MEMBER_LINE_NAME = 'member'

    def making_members_table(self):
        users = f'''CREATE TABLE IF NOT EXISTS {self.NAME_OF_TABLE}(
                      {self.IDENTIFIER_LINE_NAME} int,
                      {self.IDENTIFIER_MEMBER_LINE_NAME} str,
                      FOREIGN KEY ({self.IDENTIFIER_LINE_NAME})  REFERENCES {UsersDB.NAME_OF_TABLE} ({UsersDB.IDENTIFIER_LINE_NAME})
                      );'''
        self.execute(users, commit=True)

    def get_all_members(self, user_id: int):
        command = f'''SELECT {self.IDENTIFIER_MEMBER_LINE_NAME} FROM {self.NAME_OF_TABLE} WHERE {self.IDENTIFIER_LINE_NAME} = ?;'''
        f = self.execute(command, (user_id,), fetch_all=True)
        if f is None:
            return ()
        return f

    def delete_member(self, user_id: int, member_id:int):
        command = f'DELETE FROM {self.NAME_OF_TABLE} WHERE {self.IDENTIFIER_LINE_NAME} = ? and {self.IDENTIFIER_MEMBER_LINE_NAME} = ?;'
        self.execute(command, (user_id, member_id), commit=True)

    def add_member(self, user_id: int, member_id: int):
        command = f'''INSERT INTO {self.NAME_OF_TABLE} (
                    {self.IDENTIFIER_LINE_NAME},
                    {self.IDENTIFIER_MEMBER_LINE_NAME}) VALUES (?, ?);'''

        self.execute(command, (user_id, member_id), commit=True)




