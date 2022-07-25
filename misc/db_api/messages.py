import dataclasses

from .sessions import DBBaseObject


@dataclasses.dataclass
class SectionText:
    section: str = None
    text: str = None
    requires: str = None




class MessagesDB(DBBaseObject):
    NAME_OF_TABLE = 'messages'
    SECTION_LINE_NAME = 'section'
    TEXT_LINE_NAME = 'text'
    REQUIRES_LINE_NAME = 'requires'


    def making_messages_table(self):
        users = f'''CREATE TABLE IF NOT EXISTS {self.NAME_OF_TABLE}(
                    {self.SECTION_LINE_NAME} str NOT NULL,
                    {self.TEXT_LINE_NAME} str,
                    {self.REQUIRES_LINE_NAME} str,
                    UNIQUE({self.SECTION_LINE_NAME})
                    );'''
        self.execute(users, commit=True)

    def update_section(self, section: str, text: str):

        command = f'''UPDATE {self.NAME_OF_TABLE} SET {self.TEXT_LINE_NAME} = ? WHERE {self.SECTION_LINE_NAME} = ?;'''

        self.execute(command, (text, section), commit=True)

    def get_section_text(self, section: str):
        command = f'''SELECT {self.TEXT_LINE_NAME} FROM {self.NAME_OF_TABLE} WHERE {self.SECTION_LINE_NAME} = ?;'''
        f = self.execute(command, (section,), fetch_one=True)
        if f is None:
            return ()
        return f[0]

    def get_section(self, section: str):
        command = f'''SELECT * FROM {self.NAME_OF_TABLE} WHERE {self.SECTION_LINE_NAME} = ?;'''
        f = self.execute(command, (section,), fetch_one=True)
        if f is None:
            return ()
        return SectionText(*f)

    def add_section(self, section: str, text: str, requires: str =''):
        command = f'''INSERT OR IGNORE INTO {self.NAME_OF_TABLE}({self.SECTION_LINE_NAME}, {self.TEXT_LINE_NAME}, {self.REQUIRES_LINE_NAME}) VALUES(?, ?, ?);'''
        self.execute(command, (section, text, requires), commit=True)

    def get_sections(self) -> list[SectionText]:
        command = f'''SELECT * FROM {self.NAME_OF_TABLE};'''
        f = self.execute(command, fetch_all=True)
        return map(lambda x: SectionText(*x), f)





