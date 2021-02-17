import random

import db.mongo_db as mdb
from events.interface.actions import allfuncs
from events.vkbot_auth import vk_sessionGroup, config
from exceptions.user_exceptions import *


# Определение запрашиваемой команды
def parse(event):
    try:
        command = ""
        i = 0
        while event.object['message']['payload'][i] != "/":
            i += 1
        while event.object['message']['payload'][i] != "\"":
            command += event.object['message']['payload'][i]
            i += 1
        return command
    except KeyError:
        return None


# Проверяет наличие пользователя в базе, иначе - добавление
def check_user(event):
    user_id = event.object['message']['from_id']
    check = mdb.users_clt.find_one({'user_id': user_id})

    # Добавление пользователя в базу, в случае отсутствия
    if not check:
        mdb.insert_user(user_id)
        return mdb.users_clt.find_one({'user_id': user_id})
    else:
        return check


# Обработка сообщения
def message_processing(event):
    chat = 'chat'

    # Получение данных о пользователе
    user = check_user(event)
    state = user[chat]['state']

    if state is None:
        # Вывод главного меню
        allfuncs['/start'](user, event)
    else:
        # Определение запрашиваемой команды
        command = parse(event)

        # Выполнение пункта меню
        try:
            '''
                Решить, как избавиться
            '''
            # if state == "/ask_admin" and command is None:
            #     allfuncs[state](user, event)
            #
            # # Рассмотреть случай удаления вопроса
            # elif state == "/ask_identify" and command is not None:
            #     allfuncs[state](user, event, command)
            #
            # elif state == "/identify" and command is None:
            #     allfuncs[state](user, event)
            #
            # elif state == "/get_all" and command is None:
            #     allfuncs[state](user, event)
            #
            # elif state == "/get_series" and command is None:
            #     allfuncs[state](user, event)
            # elif state == "/get_series""/command is None:
            #     person_photos = allfuncs[command]
            if command is None:
                allfuncs[state](user, event)
            else:
                allfuncs[command](user, event)
        except KeyError:
            vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                     'message': random.choice(config.get(chat).get('failure_phrases')),
                                                     'random_id': 0})
            allfuncs[state](user, event)

        except UnexpectedRequestError:
            vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                     'message': random.choice(config.get(chat).get('failure_phrases')),
                                                     'random_id': 0})
            parent = config.get('chat').get(state).get('parent')
            allfuncs[parent](user, event)

        except (InvalidPhotoError, NotFoundError, PhotoCountError, FaceDataError) as error:
            vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                     'message': error.message,
                                                     'random_id': 0})
            parent = config.get('chat').get(state).get('parent')
            allfuncs[parent](user, event)
