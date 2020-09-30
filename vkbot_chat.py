import random

import vkbot_photo
import mongo_db as mdb
from vkbot_auth import config, id_group, vk_sessionGroup, upload
import interface
from user_exceptions import *

'''
def text_processing(user, event):
   """
        Оценка текста сообщения пользователя по предыдущему выбору, списку команд и ответу бота
   """

   text = event.object['message']['text']


   # Список 'start'
    elif last_list == 0:
    keyboard = vkbot_chat.Create_board('start')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('start').get('intro') +
                                                        config.get('chat').get('menu').get('start').get('item1') +
                                                        config.get('chat').get('menu').get('start').get('item2') +
                                                        config.get('chat').get('menu').get('start').get('item3') +
                                                        config.get('chat').get('menu').get('start').get('item4') +
                                                        config.get('chat').get('menu').get('start').get('item5'),
                                             'random_id': 0, 'keyboard': keyboard})
    last_list = 'start'
    continue

elif last_list == 'start' and text != 'закрыть клавиатуру':
if text == 'поступающим' or text == '1':
    keyboard = vkbot_chat.Create_board('item1')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item1').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('item1').get(
                                                            'item1') +
                                                        config.get('chat').get('menu').get('item1').get(
                                                            'item2') +
                                                        config.get('chat').get('menu').get('item1').get(
                                                            'item3') +
                                                        config.get('chat').get('menu').get('item1').get(
                                                            'item4'),
                                             'random_id': 0, 'keyboard': keyboard})
    last_list = 'item1'
elif text == 'первокурсникам' or text == '2':
    keyboard = vkbot_chat.Create_board('item2')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item2').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('item2').get(
                                                            'item1') +
                                                        config.get('chat').get('menu').get('item2').get(
                                                            'item2'),
                                             'random_id': 0, 'keyboard': keyboard})
    last_list = 'item2'
elif text == 'обучающимся' or text == '3':
    keyboard = vkbot_chat.Create_board('item3')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item3').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('item3').get(
                                                            'item1') +
                                                        config.get('chat').get('menu').get('item3').get(
                                                            'item2') +
                                                        config.get('chat').get('menu').get('item3').get(
                                                            'item3') +
                                                        config.get('chat').get('menu').get('item3').get(
                                                            'item4'),
                                             'random_id': 0, 'keyboard': keyboard})
    last_list = 'item3'
elif text == 'дополнительные возможности бота' or text == '4':
    keyboard = vkbot_chat.Create_board('item4')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item4').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('item4').get(
                                                            'item1'),
                                             'random_id': 0, 'keyboard': keyboard})
    last_list = 'item4'
elif text == 'задать вопрос администратору сообщества' or text == '5':
    keyboard = vkbot_chat.Create_board('item5')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item5'),
                                             'random_id': 0, 'keyboard': keyboard})
    last_list = 'item5'
elif text != '':
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('error'),
                                             'random_id': 0})
    keyboard = vkbot_chat.Create_board('start')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('start').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item1') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item2') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item3') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item4') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item5'),
                                             'random_id': 0, 'keyboard': keyboard})
continue
# Список 'item1'
elif last_list == 'item1' and text != 'закрыть клавиатуру':
if text == 'буклеты нияу мифи' or text == '1':
    keyboard = vkbot_chat.Create_board('закрыть клавиатуру')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item1').get(
                                                 'booklet'),
                                             'random_id': 0, 'keyboard': keyboard})
elif text == 'часто задаваемые вопросы' or text == '2':
    keyboard = vkbot_chat.Create_board('закрыть клавиатуру')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item1').get(
                                                 'article'),
                                             'random_id': 0, 'keyboard': keyboard})
elif text == 'студенты мифи об иикс' or text == '3':
    keyboard = vkbot_chat.Create_board('закрыть клавиатуру')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item1').get(
                                                 'about'),
                                             'random_id': 0, 'keyboard': keyboard})
elif text == 'доп.материалы для абитуриентов' or text == '4':
    keyboard = vkbot_chat.Create_board('закрыть клавиатуру')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item1').get(
                                                 'resource'),
                                             'random_id': 0, 'keyboard': keyboard})
elif text == 'назад':
    keyboard = vkbot_chat.Create_board('start')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('start').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item1') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item2') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item3') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item4') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item5'),
                                             'random_id': 0, 'keyboard': keyboard})
    last_list = 'start'
elif text != '':
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('error'),
                                             'random_id': 0})
    keyboard = vkbot_chat.Create_board('item1')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item1').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('item1').get(
                                                            'item1') +
                                                        config.get('chat').get('menu').get('item1').get(
                                                            'item2') +
                                                        config.get('chat').get('menu').get('item1').get(
                                                            'item3') +
                                                        config.get('chat').get('menu').get('item1').get(
                                                            'item4'),
                                             'random_id': 0, 'keyboard': keyboard})
continue
# Список 'item2'
elif last_list == 'item2' and text != 'закрыть клавиатуру':
if text == 'инструкция по применению' or text == '1':
    keyboard = vkbot_chat.Create_board('закрыть клавиатуру')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item2').get('ipp'),
                                             'random_id': 0, 'keyboard': keyboard})
elif text == 'памятка первокурсника' or text == '2':
    keyboard = vkbot_chat.Create_board('закрыть клавиатуру')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item2').get('note'),
                                             'random_id': 0, 'keyboard': keyboard})
elif text == 'назад':
    keyboard = vkbot_chat.Create_board('start')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('start').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item1') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item2') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item3') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item4') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item5'),
                                             'random_id': 0, 'keyboard': keyboard})
    last_list = 'start'
elif text != '':
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('error'),
                                             'random_id': 0})
    keyboard = vkbot_chat.Create_board('item2')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item2').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('item2').get(
                                                            'item1') +
                                                        config.get('chat').get('menu').get('item2').get(
                                                            'item2'),
                                             'random_id': 0, 'keyboard': keyboard})
continue
# Список 'item3'
elif last_list == 'item3' and text != 'закрыть клавиатуру':
if text == 'расписание' or text == '1':
    keyboard = vkbot_chat.Create_board('закрыть клавиатуру')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': "Раздел в разработке",
                                             'random_id': 0, 'keyboard': keyboard})
elif text == 'ближайшие мероприятия' or text == '2':
    keyboard = vkbot_chat.Create_board('закрыть клавиатуру')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': "Раздел в разработке",
                                             'random_id': 0, 'keyboard': keyboard})
elif text == 'приказы' or text == '3':
    keyboard = vkbot_chat.Create_board('закрыть клавиатуру')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': "Раздел в разработке",
                                             'random_id': 0, 'keyboard': keyboard})
elif text == 'контакты' or text == '4':
    keyboard = vkbot_chat.Create_board('закрыть клавиатуру')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': "Раздел в разработке",
                                             'random_id': 0, 'keyboard': keyboard})
elif text == 'назад':
    keyboard = vkbot_chat.Create_board('start')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('start').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item1') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item2') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item3') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item4') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item5'),
                                             'random_id': 0, 'keyboard': keyboard})
    last_list = 'start'
elif text != '':
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('error'),
                                             'random_id': 0})
    keyboard = vkbot_chat.Create_board('item3')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item3').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('item3').get(
                                                            'item1') +
                                                        config.get('chat').get('menu').get('item3').get(
                                                            'item2') +
                                                        config.get('chat').get('menu').get('item3').get(
                                                            'item3') +
                                                        config.get('chat').get('menu').get('item3').get(
                                                            'item4'),
                                             'random_id': 0, 'keyboard': keyboard})
continue
# Список 'item4'
elif last_list == 'item4' and text != 'закрыть клавиатуру':
if text == 'искать фотографии' or text == '1':
    attachments = []
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('photo').get(
                                                 'warning'),
                                             'random_id': 0})
    message = upload.photo_messages(f'{config.get("media_folder").get("name")}\\'
                                    f'{config.get("media_folder").get("example")}\\' +
                                    'example.jpg')[0]
    attachments.append('photo{}_{}'.format(message['owner_id'], message['id']))
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': 'Образец:', 'random_id': 0,
                                             'attachment': ','.join(attachments)})
elif text == 'назад':
    keyboard = vkbot_chat.Create_board('start')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('start').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item1') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item2') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item3') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item4') +
                                                        config.get('chat').get('menu').get('start').get(
                                                            'item5'),
                                             'random_id': 0, 'keyboard': keyboard})
    last_list = 'start'
elif text != '':
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('error'),
                                             'random_id': 0})
    keyboard = vkbot_chat.Create_board('item4')
    vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                             'message': config.get('chat').get('menu').get('item4').get(
                                                 'intro') +
                                                        config.get('chat').get('menu').get('item4').get(
                                                            'item1'),
                                             'random_id': 0, 'keyboard': keyboard})
continue
# Список 'item5'
elif last_list == 'item5' and text != 'закрыть клавиатуру':
vk_sessionGroup.method('messages.markAsAnsweredConversation',
                       {'peer_id': -event.object['message']['from_id'], 'answered': 0,
                        'group_id': get_json('credentials').get('group').get('id_group')})
last_list = 'start'
elif text == 'закрыть клавиатуру':
last_list = 0
keyboard = vkbot_chat.Create_board(text)
vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                         'message': config.get('chat').get('menu').get('end'),
                                         'random_id': 0, 'keyboard': keyboard})

'''


'''
# Обработка вложений-изображений
def photo_type(user, event):
    """
        Проверка контекста выбора пользователя или ответа бота на кол-во фотографий в сообщении
        Проверка намерения с вложением пользователя
    """

    if len(event.object['message']['attachments']) == 1 and event.object['message']['attachments'][0]["type"] == 'photo':
        search_person(user, event)

    else:
        pass
        """
            flag = False
            for item in range(len(event.object['message']['attachments'])):
                if event.object['message']['attachments'][item]["type"] == 'photo':
                    flag = True
                else:
                    flag = False
                    break
            if flag:
                vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                                         'message': config.get('chat').get('photo').get('warning'),
                                                         'random_id': 0})
            else:
                vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                                         'message': config.get('chat').get('menu').get('error'),
                                                         'random_id': 0})
                keyboard = Create_board('start')
                vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                                         'message': config.get('chat').get('menu').get('start').get(
                                                             'intro') +
                                                                    config.get('chat').get('menu').get('start').get(
                                                                        'item1') +
                                                                    config.get('chat').get('menu').get('start').get(
                                                                        'item2') +
                                                                    config.get('chat').get('menu').get('start').get(
                                                                        'item3') +
                                                                    config.get('chat').get('menu').get('start').get(
                                                                        'item4') +
                                                                    config.get('chat').get('menu').get('start').get(
                                                                        'item5'),
                                                         'random_id': 0, 'keyboard': keyboard})
        """


def attachments_processing(user, event):
    """
        Подразумевается, что в сообщении вложения одного типа, иначе - неопределенность
    """
    attach_type = event.object['message']['attachments'][0]["type"]

    try:
        for attachment in event.object['message']['attachments']:
            if not attachment['type'] == attach_type:
                raise BotUncertaintyError(random.choice(config.get('chat').get('failure_phrases')))
        """
            Проверка намерения с вложением пользователя
        """
        if attach_type == "photo":
            photo_type(user, event)

    except BotUncertaintyError as error:
        vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'],
                                                 'message': error.message, 'random_id': 0})
'''


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
                                             'message': config.get('chat').get('abitur').get('objects').get('ipp'),
                                             'random_id': 0})


def notes(user, event, default='exe'):
    vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                             'message': config.get('chat').get('abitur').get('objects').get('notes'),
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


# Проверяет наличие пользователя в базе, иначе - добавление
def check_user(event):
    user_id = event.object['message']['from_id']
    check = mdb.users.find_one({'user_id': user_id})

    # Добавление пользователя в базу, в случае отсутствия
    if not check:
        mdb.insert_user(mdb.users, event)
        return mdb.users.find_one({'user_id': user_id})
    else:
        return check


# Обработка сообщения
def message_processing(event):
    # Получение данных о пользователе
    user = check_user(event)

    if user['chat']['state'] is None:
        # Вывод главного меню
        allfuncs['start'](user, event, 'exe')
    else:
        # Выполнение пункта меню
        state = user['chat']['state']
        try:
            allfuncs[state](user, event, 'agent')

        except KeyError:
            chat = 'chat'
            vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                     'message': random.choice(config.get(chat).get('failure_phrases')),
                                                     'random_id': 0})

            allfuncs[state](user, event, 'exe')
            '''
                Ошибка кол-ва параметров функции (экономия памяти)
            '''

        except UnexpectedRequestError:
            chat = 'chat'
            vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                     'message': random.choice(config.get(chat).get('failure_phrases')),
                                                     'random_id': 0})
            parent = config.get('chat').get(state).get('parent')
            allfuncs[parent](user, event, 'exe')

        except (InvalidPhotoError, NotFoundError, PhotoCountError, FaceDataError) as error:
            vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                     'message': error.message,
                                                     'random_id': 0})
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

"""
        if len(event.object['message']['attachments']) != 0:
        # Обработка вложений сообщения
        attachments_processing(user, event)

        else:
        # Обработка текста сообщения
        text_processing(user, event)
            Изменение в базе данных о последнем действии пользователя
"""
