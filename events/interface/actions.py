from db import mongo_db as mdb
from events.vkbot_auth import config, id_group, vk_sessionGroup
from events.interface import interface
from events import vkbot_photo
from exceptions.user_exceptions import *


# Главное меню
def start(user, event):
    command = "/start"

    interface.print_menu(user, command)
    mdb.set_user_state(user, command)
    return


# Назад
def come_back(user, event):
    state = user['chat']['state']
    parent = config.get('chat').get(state).get('parent')
    allfuncs[parent](user, event)
    return


# Возможности бота
def ability(user, event):
    command = "/ability"
    interface.print_menu(user, command)
    mdb.set_user_state(user, command)
    return


# Задать вопрос
def ask_admin(user, event):
    command = "/ask_admin"

    state = user['chat']['state']
    if state == command:
        vk_sessionGroup.method('messages.markAsAnsweredConversation',
                               {'peer_id': -user['user_id'], 'answered': 0,
                                'group_id': id_group})
    else:
        interface.print_menu(user, command)
        mdb.set_user_state(user, command)
    return


# Помощь
def help_list(user, event):
    command = "/help_list"

    interface.print_menu(user, command)
    interface.print_text(user, config.get('chat').get(command).get('help'))
    mdb.set_user_state(user, command)
    return


# Искать фотографии
def search_photos(user, event):
    command = '/search_photos'

    # user = mdb.get_user_data(user['user_id'])
    # if user['identify'] != 0 and user['identify'] != 1:
    #     allfuncs['/ask_identify'](user, event)
    #     return

    interface.print_menu(user, command)
    mdb.set_user_state(user, command)
    return


'''
# Запрос на идентификацию личности
def ask_identify(user, event):
    command = '/ask_identify'

    interface.print_menu(user, command)
    mdb.set_user_state(user, command)
    mdb.set_user_identify(user, 0)
    return


# Идентификация личности
def identify(user, event):
    command = '/identify'

    user_id = user['user_id']

    state = user['chat']['state']
    if state == command:
        if len(event.object['message']['attachments']) == 0:
            raise UnexpectedRequestError

        face_data = vkbot_photo.get_user_photo(event)
        mdb.set_user_embedding(user, face_data[0]['emb'])
        mdb.set_user_identify(user, 1)

        text = config.get('chat').get('success').get('photo').get('identify')
        vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                 'message': text, 'random_id': 0})
        parent = config.get('chat').get(command).get('parent')
        allfuncs[parent](user, event)
    else:
        user_data = mdb.get_user_data(user_id)
        if user['identify'] == 1:
            text = config.get('chat').get('errors').get('photo').get('identify')
            vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                     'message': text, 'random_id': 0})
        else:
            interface.print_menu(user, command)
            mdb.set_user_state(user, command)
    return
'''


# Получить все фотографии (архив)
def get_photos(user, event):
    command = '/get_photos'

    user_id = event.object['message']['from_id']
    state = user['chat']['state']

    if state == command:
        if len(event.object['message']['attachments']) == 0:
            raise UnexpectedRequestError

        face_data = vkbot_photo.get_user_photo(event)
        person_photos = vkbot_photo.search_person(user_id, face_data)
        vkbot_photo.send_archive_to_user(person_photos, user_id)

        parent = config.get('chat').get(command).get('parent')
        allfuncs[parent](user, event)
        return
    else:
        vkbot_photo.send_example(user_id, command)
        mdb.set_user_state(user, command)
    return


# Инструкция по поиску фотографий
def help_search_photos(user, event):
    command = 'help_search_photos'
    interface.print_text(user, config.get('chat').get('/help_search_photos'))
    return


def delete_user_data(user, event):
    user_id = user['user_id']
    mdb.delete_user(user_id)

    text = config.get('chat').get('success').get('photo').get('delete_user_data')
    vk_sessionGroup.method('messages.send', {'user_id': user_id,
                                             'message': text, 'random_id': 0})


allfuncs = {'/start': start,
            '/come_back': come_back,
            '/ability': ability,
            '/ask_admin': ask_admin,
            '/help_list': help_list,
            '/delete_user_data': delete_user_data,
            '/search_photos': search_photos,
            '/get_photos': get_photos,
            '/help_search_photos': help_search_photos,
            }

# '/ask_identify': ask_identify,
# '/identify': identify,