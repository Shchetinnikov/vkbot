from exceptions.user_exceptions import *
from events import vkbot_photo
from db import mongo_db as mdb
from events.vkbot_auth import config, id_group, vk_sessionGroup, upload
from events.interface import interface


# def help_search_photos(user, event, default='exe'):
#     command = 'help_search_photos'
#     interface.print_text(user, command)
#     return
#
#
# def get_all_photos(user, event, default='exe'):
#     command = 'get_all_photos'
#
#     if default == 'exe':
#         vkbot_photo.send_example(user['user_id'], command)
#         mdb.set_user_state(user, command)
#     elif default == 'agent':
#         text = event.object['message']['text']
#         try:
#             command = config.get('chat').get('get_all_photos').get('intents').get(text)
#             allfuncs[command](user, event, 'exe')
#         except KeyError:
#             parent = config.get('chat').get('get_all_photos').get('parent')
#             mdb.set_user_state(user, parent)
#             if event.object['message']['text'] and len(event.object['message']['attachments']) == 0:
#                 raise UnexpectedRequestError
#
#             user_id = event.object['message']['from_id']
#
#             face_data = vkbot_photo.get_user_photo(event)
#             person_photos = vkbot_photo.search_person(user_id, face_data)
#             vkbot_photo.send_photos_to_user(person_photos, user_id)
#
#             allfuncs[parent](user, event, 'exe')
#     return
#
#
# def get_series_photos(user, event, default='exe'):
#     command = 'get_series_photos'
#
#     if default == 'exe':
#         vkbot_photo.send_example(user['user_id'], command)
#         mdb.set_user_state(user, command)
#     elif default == 'agent':
#         text = event.object['message']['text']
#         try:
#             command = config.get('chat').get('get_series_photos').get('intents').get(text)
#             allfuncs[command](user, event, 'exe')
#         except KeyError:
#             parent = config.get('chat').get('get_series_photos').get('parent')
#             mdb.set_user_state(user, parent)
#             if event.object['message']['text'] and len(event.object['message']['attachments']) == 0:
#                 raise UnexpectedRequestError
#
#             face_data = vkbot_photo.get_user_photo(event)
#             person_photos = vkbot_photo.search_person(face_data)
#             user_id = event.object['message']['from_id']
#             vkbot_photo.send_photos_to_user(person_photos, user_id)
#
#             allfuncs[parent](user, event, 'exe')
#     return
#
#
# def search_photos(user, event, default='exe'):
#     command = 'search_photos'
#
#     if default == 'exe':
#         user = mdb.get_user_data(user['user_id'])
#
#         if user['identify'] != 0 and user['identify'] != 1:
#             allfuncs['ask_identify'](user, event, default='exe')
#             return
#
#         interface.print_menu(user, command)
#         mdb.set_user_state(user, command)
#     elif default == 'agent':
#         text = event.object['message']['text']
#         command = config.get('chat').get('search_photos').get('intents').get(text)
#         allfuncs[command](user, event, 'exe')
#
#
# def help_list(user, event, default='exe'):
#     command = 'help_list'
#
#     if default == 'exe':
#         interface.print_menu(user, command)
#         interface.print_text(user, 'help')
#         mdb.set_user_state(user, command)
#     elif default == 'agent':
#         text = event.object['message']['text']
#         try:
#             command = config.get('chat').get('help_list').get('intents').get(text)
#             allfuncs[command](user, event, 'exe')
#         except KeyError:
#             parent = config.get('chat').get('help_list').get('parent')
#             mdb.set_user_state(user, parent)
#             raise UnexpectedRequestError
#     return
#
#
# def ask_admin(user, event, default='exe'):
#     command = 'ask_admin'
#
#     if default == 'exe':
#         interface.print_menu(user, command)
#         mdb.set_user_state(user, command)
#     elif default == 'agent':
#         text = event.object['message']['text']
#         try:
#             command = config.get('chat').get('ask_admin').get('intents').get(text)
#             allfuncs[command](user, event, 'exe')
#         except KeyError:
#             vk_sessionGroup.method('messages.markAsAnsweredConversation',
#                                    {'peer_id': -user['user_id'], 'answered': 0,
#                                     'group_id': id_group})
#
#
# def ask_identify(user, event, default='exe'):
#     command = 'ask_identify'
#
#     if default == 'exe':
#         interface.print_menu(user, command)
#         mdb.set_user_state(user, command)
#
#     elif default == 'agent':
#         text = event.object['message']['text']
#         parent = config.get('chat').get('ask_identify').get('parent')
#         mdb.set_user_state(user, parent)
#         try:
#             if text == "Да":
#                 allfuncs['identify'](user, event, 'exe')
#                 return
#             elif text == "Нет":
#                 mdb.set_user_identify(user, 0)
#                 allfuncs[parent](user, event, 'exe')
#         except KeyError:
#             raise UnexpectedRequestError
#
#
# def identify(user, event, default='exe'):
#     command = 'identify'
#
#     if default == 'exe':
#         interface.print_menu(user, command)
#         mdb.set_user_state(user, command)
#     elif default == 'agent':
#         text = event.object['message']['text']
#         try:
#             command = config.get('chat').get('identify').get('intents').get(text)
#             allfuncs[command](user, event, 'exe')
#         except KeyError:
#             parent = config.get('chat').get('identify').get('parent')
#             mdb.set_user_state(user, parent)
#             if event.object['message']['text'] and len(event.object['message']['attachments']) == 0:
#                 raise UnexpectedRequestError
#
#             face_data = vkbot_photo.get_user_photo(event)
#             mdb.set_user_embedding(user, face_data[0]['emb'])
#             mdb.set_user_identify(user, 1)
#
#             text = config.get('chat').get('success').get('photo').get('identify')
#             vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
#                                                      'message': text, 'random_id': 0})
#             allfuncs[parent](user, event, 'exe')
#
#
# def delete_user_data(user, event, default='exe'):
#
#     pass
#
#
# def ability(user, event, default='exe'):
#     command = 'ability'
#
#     if default == 'exe':
#         interface.print_menu(user, command)
#         mdb.set_user_state(user, command)
#     elif default == 'agent':
#         text = event.object['message']['text']
#         command = config.get('chat').get('ability').get('intents').get(text)
#         allfuncs[command](user, event, 'exe')
#
#
# def start(user, event, default='exe'):
#     command = 'start'
#
#     if default == 'exe':
#         interface.print_menu(user, command)
#         mdb.set_user_state(user, command)
#     elif default == 'agent':
#         text = event.object['message']['text']
#         command = config.get('chat').get('start').get('intents').get(text)
#         allfuncs[command](user, event, 'exe')
#
#
# def come_back(user, event, default='exe'):
#     state = user['chat']['state']
#     parent = config.get('chat').get(state).get('parent')
#     allfuncs[parent](user, event, 'exe')
#

# allfuncs = {'start': start,
#             'ability': ability,
#             'ask_admin': ask_admin,
#             "identify": identify,
#             "ask_identify": ask_identify,
#             'help_list': help_list,
#             'delete_user_data': delete_user_data,
#             'search_photos': search_photos,
#             'help_search_photos': help_search_photos,
#             'get_all_photos': get_all_photos,
#             'get_series_photos': get_series_photos,
#             'come_back': come_back,
#             }
