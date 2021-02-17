from _datetime import datetime
import random
from db import mongo_db as mdb

from timer import time_tools
from events.vkbot_auth import config, vk_sessionGroup
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


# Функция, создает интерактивные кнопки в диалоге
def Create_board(state=None):
    # keyboard = VkKeyboard(one_time=True, inline=True)
    chat = 'chat'
    keyboard = VkKeyboard(one_time=False)
    if state is None:
        return keyboard.get_empty_keyboard()

    if state == '/start':
        keyboard.add_button(config.get(chat).get(state).get('ability'), color=VkKeyboardColor.PRIMARY,
                            payload="{\"button:\": \"/ability\"}")
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('ask_admin'), color=VkKeyboardColor.PRIMARY,
                            payload="{\"button:\": \"/ask_admin\"}")
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('help_list'), color=VkKeyboardColor.PRIMARY,
                            payload="{\"button:\": \"/help_list\"}")
        keyboard = keyboard.get_keyboard()
        return keyboard

    elif state == '/ability':
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button(config.get(chat).get(state).get('search_photos'), color=VkKeyboardColor.POSITIVE,
                            payload="{\"button:\": \"/search_photos\"}")
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('come_back'), color=VkKeyboardColor.NEGATIVE,
                            payload="{\"button:\": \"/come_back\"}")
        keyboard = keyboard.get_keyboard()
        return keyboard

    elif state == '/ask_admin':
        keyboard.add_button(config.get(chat).get(state).get('come_back'), color=VkKeyboardColor.NEGATIVE,
                            payload="{\"button:\": \"/come_back\"}")
        keyboard = keyboard.get_keyboard()
        return keyboard

    elif state == "/help_list":
        keyboard.add_button(config.get(chat).get(state).get('delete_user_data'), color=VkKeyboardColor.NEGATIVE,
                            payload="{\"button:\": \"/delete_user_data\"}")
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('come_back'), color=VkKeyboardColor.NEGATIVE,
                            payload="{\"button:\": \"/come_back\"}")
        keyboard = keyboard.get_keyboard()
        return keyboard

    elif state == '/search_photos':
        # keyboard.add_button(config.get(chat).get(state).get('identify'), color=VkKeyboardColor.POSITIVE,
        #                     payload="{\"button:\": \"/identify\"}")
        # keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('get_photos'), color=VkKeyboardColor.PRIMARY,
                            payload="{\"button:\": \"/get_photos\"}")
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('help_search_photos'), color=VkKeyboardColor.PRIMARY,
                            payload="{\"button:\": \"/help_search_photos\"}")
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('come_back'), color=VkKeyboardColor.NEGATIVE,
                            payload="{\"button:\": \"/come_back\"}")
        keyboard.add_button(config.get(chat).get(state).get('start'), color=VkKeyboardColor.NEGATIVE,
                            payload="{\"button:\": \"/start\"}")
        keyboard = keyboard.get_keyboard()
        return keyboard

    # elif state == "/ask_identify":
    #     keyboard = VkKeyboard(one_time=False, inline=True)
    #     keyboard.add_button(config.get(chat).get(state).get('yes'), color=VkKeyboardColor.PRIMARY,
    #                         payload="{\"button:\": \"/identify\"}")
    #     keyboard.add_button(config.get(chat).get(state).get('no'), color=VkKeyboardColor.PRIMARY,
    #                         payload="{\"button:\": \"/search_photos\"}")
    #     keyboard = keyboard.get_keyboard()
    #     return keyboard
    #
    # elif state == "/identify":
    #     keyboard = VkKeyboard(one_time=True)
    #     keyboard.add_button(config.get(chat).get(state).get('come_back'), color=VkKeyboardColor.NEGATIVE,
    #                         payload="{\"button:\": \"/come_back\"}")
    #     keyboard.add_line()
    #     keyboard.add_button(config.get(chat).get(state).get('start'), color=VkKeyboardColor.NEGATIVE,
    #                         payload="{\"button:\": \"/start\"}")
    #     keyboard = keyboard.get_keyboard()
    #     return keyboard

    elif state == "/get_photos":
        keyboard.add_button(config.get(chat).get(state).get('come_back'), color=VkKeyboardColor.NEGATIVE,
                            payload="{\"button:\": \"/come_back\"}")
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('start'), color=VkKeyboardColor.NEGATIVE,
                            payload="{\"button:\": \"/start\"}")
        keyboard = keyboard.get_keyboard()
        return keyboard


def print_menu(user, state):
    keyboard = Create_board(state)
    if user['chat']['state'] is None:
        vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                 'message': config['chat']['greeting']['first_meeting']['hello'] +
                                                            user['first_name'] + "!\n",
                                                 'random_id': 0, 'keyboard': keyboard})
    else:
        current_date = datetime.now()
        last_greeting_date = time_tools.compound(user['chat']['last_greeting'])
        timer_threshold = time_tools.timer_threshold

        if ((current_date - last_greeting_date) >= timer_threshold) \
                or (current_date.hour >= 6 and last_greeting_date.hour < 6) \
                or (current_date.hour >= 6 and last_greeting_date.day != current_date.day):
            vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                     'message': random.choice(config['chat']['greeting']['hello']) +
                                                                user['first_name'] + "!\n",
                                                     'random_id': 0})
            mdb.update_last_greeting(user)

        vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                                 'message': config['chat'][state]['intro'],
                                                 'random_id': 0, 'keyboard': keyboard})


def print_text(user, sentences):
    text = ""
    for value in sentences.values():
        text += value
    vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                             'message': text, 'random_id': 0})
