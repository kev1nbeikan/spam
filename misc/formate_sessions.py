import json
import logging
import os
from datetime import datetime

from misc import TelethonSessionDB, PyrogramSessionDB, Session
from os.path import exists
from os import mkdir
from data.config import DIR_TO_BOTS_FILES
from .filehandlers import LocalFileHandler


def get_last_file(work_path):
    namelist = os.listdir(work_path)
    if not namelist:
        return 0
    return int(namelist[-1].split('.')[0])

def get_file_count(work_path):
    file_handler = LocalFileHandler()
    files = file_handler.listdir(work_path)
    return len(files) if files else 0


def check_member(member):
    if member is None:
        return True
    return datetime.now().timestamp() < int(member)



def check_files(dir):
    """
    Проверка на соответствие файлов на чередование .json, .session

    :param dir:
    :return:
    """
    names = os.listdir(dir)
    if names[0].endswith('.json'):
        for i in range(1, len(names) - 1, 2):
            if not names[i].endswith('.session'):
                return False
    else:
        for i in range(1, len(names), 2):
            if not names[i].endswith('.json'):
                return False
    return True


def change_telethon_type(dirs: list):

    """
    Форматирует сессии типа telethon для pyrogram и записывает их в файл new/{имя}.sessions
    :param dirs: path to files where exists .json and .sessions
    :return:
    """
    from loader import sessions_db
    for folder in dirs:
        work_path = f'{DIR_TO_BOTS_FILES}/{folder}'
        path_old = work_path + '/old'
        path_new = work_path + '/new'

        if not exists(path_new):
            mkdir(path_new)

        result = ''

        last = get_last_file(path_new)
        for filename in os.listdir(path_old):
            path_to_json = f'{path_old}/{filename}'
            if 'json' in filename:
                with open(path_to_json, 'r') as f:
                    info = json.load(f)

                bot_name = filename.replace('.json', '')

                path_to_session = f'{path_old}/{bot_name}.session'
                str_lst = str(last)
                path_to_new_session = f'{path_new}/{str_lst}.session'
                last += 1


                if exists(path_to_session) and not exists(path_to_new_session):
                    old = TelethonSessionDB(path_to_session)
                    new = PyrogramSessionDB(path_to_new_session)
                    new.making_tables()
                    old.add_in_pyrogram(new, info.get('app_id'), info.get('app_hash'))

                    s = Session(db=sessions_db,
                                name=str_lst,
                                folder=folder,
                                app_version=info.get('app_version'),
                                device_model=info.get('device'),
                                system_version=info.get('sdk'),
                                lang_code=info.get('lang_pack'),
                                ipv6=info.get('ipv6'),
                                phone_number=info.get('phone'))

                    s.write_to_db()
                    os.remove(path_to_session)
                    os.remove(path_to_json)

                else:
                    result += f'Бот {filename} не имеет файла сессии \n'

        return ''


async def check_sessions(folder, sessions_db):
    work_path = f'{DIR_TO_BOTS_FILES}/{folder}/new'
    for filename in os.listdir(work_path):
        s = Session(sessions_db, filename.replace('.session', ''), folder)
        s.load_from_db()
        if not await s.check_acc():
            s.delete()
        yield s




def load_telethon_type(dirs: list):

    """
    Форматирует сессии типа telethon для pyrogram и записывает их в файл new/{имя}.sessions
    :param dirs: path to files where exists .json and .sessions
    :return:
    """
    from loader import sessions_db
    for folder in dirs:
        work_path = f'{DIR_TO_BOTS_FILES}/{folder}'
        path_old = work_path + '/old'
        path_new = work_path + '/new'

        if not exists(path_new):
            mkdir(path_new)

        result = ''

        last = get_last_file(path_new)
        for filename in os.listdir(path_old):
            path_to_json = f'{path_old}/{filename}'
            if 'json' in filename:
                with open(path_to_json, 'r') as f:
                    info = json.load(f)

                bot_name = filename.replace('.json', '')

                path_to_session = f'{path_old}/{bot_name}.session'
                str_lst = str(last)
                path_to_new_session = f'{path_new}/{str_lst}.session'
                last += 1


                if exists(path_to_session) and not exists(path_to_new_session):
                    os.replace(path_to_session, path_to_new_session)

                    s = Session(db=sessions_db,
                                name=str_lst,
                                folder=folder,
                                app_version=info.get('app_version'),
                                device_model=info.get('device'),
                                system_version=info.get('sdk'),
                                lang_code=info.get('lang_pack'),
                                ipv6=info.get('ipv6'),
                                phone_number=info.get('phone'),
                                app_hash=info.get("app_hash"),
                                app_id=info.get("app_id"))
                    logging.info(f'{s.app_hash}, {s.app_id}')
                    s.write_to_db()
                    # os.remove(path_to_session)
                    os.remove(path_to_json)

                else:
                    result += f'Бот {filename} не имеет файла сессии \n'

        return ''

