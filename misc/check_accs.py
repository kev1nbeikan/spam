import os
from zipfile import ZipFile
from misc import Session
from os import listdir
from data import DIR_TO_BOTS_FILES

def check_accs(sessions) -> bool:
    """
    Проверяет все аккаунты в папке
    :param sessions: папка с сессиями
    :return:
    """
    for s in listdir(DIR_TO_BOTS_FILES + '/' + sessions):
        session = Session(name=s, folder=sessions)
        session.check_acc()
        yield (session.ban_info, session.err_info)


def unpack_files(name):
    with ZipFile(name, 'w') as file:
        lst = map(lambda x: x.filename, file.infolist())
        for zi in lst:
            if True:
                pass





