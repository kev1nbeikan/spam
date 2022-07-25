
# Здесь все хендлеры для загрузки архива с ботами

import datetime
import logging
import os
import stat
import zipfile
from zipfile import ZipFile

from aiogram import types
# from unrar.rarfile import RarFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
# from unrar import rarfile

from loader import dp, sessions_db
from data import DIR_TO_BOTS_FILES, FilesUploadingStrings, SessionHandleStrings, GettingGroupsStrings, GettingMessageStrings
from misc import change_telethon_type, check_sessions, LocalFileHandler, check_file_name, load_telethon_type
from keyboard import check_sessions_data, next_step, is_correct
from .states import Spam


@dp.callback_query_handler(Text(GettingMessageStrings.CHANGE_QUERY), state=Spam.get_message)
@dp.message_handler(Text(equals=GettingGroupsStrings.NEXT_STEP), state=Spam.get_bot_files)
async def message_input(message: types.Message):
    await Spam.get_message.set()
    await message.answer(GettingMessageStrings.ASK_MESSAGE, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=['document'], state=Spam.get_bot_files)
async def get_file(message: types.Message):
    file_handler = LocalFileHandler()

    user = str(message.from_user.id)
    user_dir = f'{DIR_TO_BOTS_FILES}/{user}'

    file_handler.mkdir(user_dir)
    if message.document.file_size >= 104857600:
        await message.answer(FilesUploadingStrings.WRONG_SIZE_FILE)
        return
    doc = message.document.file_name
    path_to_extract = user_dir

    name_of_ctlg = f'{datetime.datetime.now().utcnow():%d.%m.%y.t%H.%M.%S}'

    # if doc.endswith('.rar'):
        # # создание пути до файла, скачивание документа
        # path_to_archive = path_to_extract + f'/{name_of_ctlg}.zip'
        # await message.document.download(path_to_archive)
        #
        # # открытие архива
        # if rarfile.is_rarfile(path_to_archive):
        #     zp = rarfile.RarFile(path_to_archive)
        # else:
        #     await message.answer(FilesUploadingStrings.WRONG_TYPE_FILE)
        #     return
        #
        # path_old = path_to_extract + '/old'
        #
        # # проверка на кривые файлы
        # if zp.testrar() is None:
        #
        #     file_handler.mkdir(path_old)
        #
        #     namelist = zp.namelist()
        #
        #     msg = await message.answer(FilesUploadingStrings.CHECKING_FILES + '.')
        #     logging.info(namelist)
        #     # проверка архива на соответствие шаблону
        #     if not all((check_file_name(filename) for filename in namelist)):
        #         await msg.edit_text(FilesUploadingStrings.WRONG_CONTENT)
        #         await message.answer_photo(caption=FilesUploadingStrings.EXAMPLE_OF_ORDER_ZIP,
        #                                    photo=FilesUploadingStrings.FILE_SERVER_ID_ASK_ZIP)
        #
        #         # zp._close()
        #         file_handler.remove(path_to_archive)
        #         return
        #
        #     # сохрание на сервер
        #     file_handler.zp_extract(zp, path_old)
        #     msg = await msg.edit_text(msg.text + '.')
        #     result = load_telethon_type([f'{user}'])
        #
        #     # кнопка для проверки акканутов
        #     inline = InlineKeyboardMarkup().add(
        #         InlineKeyboardButton(FilesUploadingStrings.CHECK_ACCS,
        #                              callback_data=check_sessions_data.new(folder=f'{user}')))
        #
        #     msg = await msg.edit_text(msg.text + '.')
        #
        #     if result:
        #         await msg.edit_text(FilesUploadingStrings.SUCCESS_WITH_ISSUE + '\n' + result, reply_markup=inline)
        #     else:
        #         await msg.edit_text(FilesUploadingStrings.SUCCESS, reply_markup=inline)
        #     zp.close()
        #     file_handler.remove(path_to_archive)

    if doc.endswith('.zip'):
        # создание пути до файла, скачивание документа
        path_to_archive = path_to_extract + f'/{name_of_ctlg}.zip'
        await message.document.download(path_to_archive)

        # открытие архива
        if zipfile.is_zipfile(path_to_archive):
            zp = ZipFile(path_to_archive)
        else:
            await message.answer(FilesUploadingStrings.WRONG_TYPE_FILE)
            return

        path_old = path_to_extract + '/old'

        # проверка на кривые файлы
        if zp.testzip() is None:

            file_handler.mkdir(path_old)

            namelist = zp.namelist()

            msg = await message.answer(FilesUploadingStrings.CHECKING_FILES + '.')
            logging.info(namelist)
            # проверка архива на соответствие шаблону
            if not all((check_file_name(filename) for filename in namelist)):
                await msg.edit_text(FilesUploadingStrings.WRONG_CONTENT)
                await message.answer_photo(caption=FilesUploadingStrings.EXAMPLE_OF_ORDER_ZIP,
                                           photo=FilesUploadingStrings.FILE_SERVER_ID_ASK_ZIP)

                zp.close()
                file_handler.remove(path_to_archive)
                return

            # сохрание на сервер
            file_handler.zp_extract(zp, path_old)
            msg = await msg.edit_text(msg.text + '.')
            result = load_telethon_type([f'{user}'])

            # кнопка для проверки акканутов
            inline = InlineKeyboardMarkup().add(
                InlineKeyboardButton(FilesUploadingStrings.CHECK_ACCS,
                                     callback_data=check_sessions_data.new(folder=f'{user}')))

            msg = await msg.edit_text(msg.text + '.')


            if result:
                await msg.edit_text(FilesUploadingStrings.SUCCESS_WITH_ISSUE + '\n' + result, reply_markup=inline)
            else:
                await msg.edit_text(FilesUploadingStrings.SUCCESS, reply_markup=inline)
            zp.close()
            file_handler.remove(path_to_archive)
    else:
        await message.answer(FilesUploadingStrings.WRONG_TYPE_FILE)


@dp.callback_query_handler(check_sessions_data.filter(), state=Spam.get_bot_files)
async def checking_accs(call: types.CallbackQuery, callback_data : dict):
    folder = callback_data.get('folder')
    msg = await call.message.answer(FilesUploadingStrings.CHECKING_BOTS.format(count=0))
    k = len(os.listdir(f'{DIR_TO_BOTS_FILES}/{folder}/new'))
    c = k
    check_count = 0
    result = ''
    async for s in check_sessions(folder, sessions_db):
        if s.ban_info == SessionHandleStrings.BOT_WORK:
            pass
        else:
            # logging.info(s.err_info)
            k -= 1
        check_count += 1
        await msg.edit_text(FilesUploadingStrings.CHECKING_BOTS.format(count=check_count))

        s.write_to_db()

    result += f'{k}/{c} работают\n'
    if k > 0:
        await call.message.answer(result, reply_markup=next_step)
    else:
        await call.message.answer(result)
    await call.answer()


