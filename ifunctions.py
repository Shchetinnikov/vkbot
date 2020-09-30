from user_exceptions import *
import vkbot_photo
import mongo_db as mdb
from vkbot_auth import config, id_group, vk_sessionGroup, upload
import interface


def search_photos(user, event, default='exe'):
    command = 'search_photos'

    if default == 'exe':
        attachments = []
        vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                 'message': config.get('chat').get('errors').get('photo').get('one_person'),
                                                 'random_id': 0})
        message = upload.photo_messages(f'{config.get("media_folder").get("name")}\\' +
                                        f'{config.get("media_folder").get("folders").get("photo_example")}\\' +
                                        'example.jpg')[0]
        attachments.append('photo{}_{}'.format(message['owner_id'], message['id']))
        vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                 'message': 'Образец:', 'random_id': 0,
                                                 'attachment': ','.join(attachments)})
        mdb.set_user_state(mdb.users, user, command)

    elif default == 'agent':
        if event.object['message']['text'] and len(event.object['message']['attachments']) == 0:
            raise UnexpectedRequestError
        face_data = vkbot_photo.get_user_photo(event)
        person_photos = vkbot_photo.search_person(face_data)
        vkbot_photo.send_photos_to_user(person_photos, event)


def instruction_pp(user, event, default='exe'):
    vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                             'message': config.get('chat').get('fresher').get('objects').get('ipp'),
                                             'random_id': 0})


def notes(user, event, default='exe'):
    vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                             'message': config.get('chat').get('fresher').get('objects').get('notes'),
                                             'random_id': 0})


def articles(user, event, default='exe'):
    vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                             'message': config.get('chat').get('abitur').get('objects').get('articles'),
                                             'random_id': 0})


def resource(user, event, default='exe'):
    vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                             'message': config.get('chat').get('abitur').get('objects').get('resource'),
                                             'random_id': 0})


def about_mephi(user, event, default='exe'):
    vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                             'message': config.get('chat').get('abitur').get('objects').get(
                                                 'about_mephi'),
                                             'random_id': 0})


def booklets(user, event, default='exe'):
    vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                             'message': config.get('chat').get('abitur').get('objects').get('booklets'),
                                             'random_id': 0})


def help_list(user, event, default='exe'):
    pass


def ask_admin(user, event, default='exe'):
    command = 'ask_admin'

    if default == 'exe':
        vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                 'message': config.get('chat').get('ask_admin').get('intro'),
                                                 'random_id': 0})
        mdb.set_user_state(mdb.users, user, command)
    elif default == 'agent':
        command = config.get('chat').get('ask_admin').get('parent')
        vk_sessionGroup.method('messages.markAsAnsweredConversation',
                               {'peer_id': -user['user_id'], 'answered': 0,
                                'group_id': id_group})
        mdb.set_user_state(mdb.users, user, command)


def ability(user, event, default='exe'):
    command = 'ability'

    if default == 'exe':
        interface.print_menu(user, command)
        mdb.set_user_state(mdb.users, user, command)
    elif default == 'agent':
        text = event.object['message']['text']
        command = config.get('chat').get('ability').get('intents').get(text)
        allfuncs[command](user, event, 'exe')


def student(user, event, default='exe'):
    command = 'student'

    if default == 'exe':
        interface.print_menu(user, command)
        mdb.set_user_state(mdb.users, user, command)
    elif default == 'agent':
        text = event.object['message']['text']
        command = config.get('chat').get('student').get('intents').get(text)
        allfuncs[command](user, event, 'exe')


def fresher(user, event, default='exe'):
    command = 'fresher'

    if default == 'exe':
        interface.print_menu(user, command)
        mdb.set_user_state(mdb.users, user, command)
    elif default == 'agent':
        text = event.object['message']['text']
        command = config.get('chat').get('fresher').get('intents').get(text)
        allfuncs[command](user, event, 'exe')


def abitur(user, event, default='exe'):
    command = 'abitur'

    if default == 'exe':
        interface.print_menu(user, command)
        mdb.set_user_state(mdb.users, user, command)
    elif default == 'agent':
        text = event.object['message']['text']
        command = config.get('chat').get('abitur').get('intents').get(text)
        allfuncs[command](user, event, 'exe')


def start(user, event, default='exe'):
    command = 'start'

    if default == 'exe':
        interface.print_menu(user, command)
        mdb.set_user_state(mdb.users, user, command)
    elif default == 'agent':
        text = event.object['message']['text']
        command = config.get('chat').get('start').get('intents').get(text)
        allfuncs[command](user, event, 'exe')


def come_back(user, event, default='exe'):
    state = user['chat']['state']
    parent = config.get('chat').get(state).get('parent')
    allfuncs[parent](user, event, 'exe')


allfuncs = {'start': start,
            'abitur': abitur,
            'fresher': fresher,
            'student': student,
            'ability': ability,
            'ask_admin': ask_admin,
            'help': help_list,
            'booklets': booklets,
            'about_mephi': about_mephi,
            'resource': resource,
            'articles': articles,
            'instruction_pp': instruction_pp,
            'notes': notes,
            'search_photos': search_photos,
            'come_back': come_back,
            }
