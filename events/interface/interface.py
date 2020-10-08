from events.vkbot_auth import config, vk_sessionGroup
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


# Функция, создает интерактивные кнопки в диалоге
def Create_board(state):
    # keyboard = VkKeyboard(one_time=True, inline=True)
    chat = 'chat'
    keyboard = VkKeyboard(one_time=False)
    # if text == 'закрыть клавиатуру' or text == 'item5':
    #     return keyboard.get_empty_keyboard()
    if state == 'start':
        keyboard.add_button(config.get(chat).get(state).get('item1'), color=VkKeyboardColor.PRIMARY)
        keyboard.add_button(config.get(chat).get(state).get('item2'), color=VkKeyboardColor.PRIMARY)
        keyboard.add_button(config.get(chat).get(state).get('item3'), color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('item4'), color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('item5'), color=VkKeyboardColor.SECONDARY)
        keyboard.add_button(config.get(chat).get(state).get('item6'), color=VkKeyboardColor.SECONDARY)
        # keyboard.add_line()
        # keyboard.add_button('Закрыть клавиатуру', color=VkKeyboardColor.NEGATIVE)
        keyboard = keyboard.get_keyboard()
        return keyboard
    elif state == 'abitur':
        keyboard.add_button(config.get(chat).get(state).get('item1'), color=VkKeyboardColor.PRIMARY)
        keyboard.add_button(config.get(chat).get(state).get('item2'), color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('item3'), color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('item4'), color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('back'), color=VkKeyboardColor.NEGATIVE)
        # keyboard.add_button('Закрыть клавиатуру', color=VkKeyboardColor.NEGATIVE)
        keyboard = keyboard.get_keyboard()
        return keyboard
    elif state == 'fresher':
        keyboard.add_button(config.get(chat).get(state).get('item1'), color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('item2'), color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('back'), color=VkKeyboardColor.NEGATIVE)
        # keyboard.add_button('Закрыть клавиатуру', color=VkKeyboardColor.NEGATIVE)
        keyboard = keyboard.get_keyboard()
        return keyboard
    elif state == 'student':
        keyboard.add_button(config.get(chat).get(state).get('item1'), color=VkKeyboardColor.PRIMARY)
        keyboard.add_button(config.get(chat).get(state).get('item2'), color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('item3'), color=VkKeyboardColor.PRIMARY)
        keyboard.add_button(config.get(chat).get(state).get('item4'), color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('back'), color=VkKeyboardColor.NEGATIVE)
        # keyboard.add_button('Закрыть клавиатуру', color=VkKeyboardColor.NEGATIVE)
        keyboard = keyboard.get_keyboard()
        return keyboard
    elif state == 'ability':
        keyboard.add_button(config.get(chat).get(state).get('item1'), color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(config.get(chat).get(state).get('back'), color=VkKeyboardColor.NEGATIVE)
        # keyboard.add_button('Закрыть клавиатуру', color=VkKeyboardColor.NEGATIVE)
        keyboard = keyboard.get_keyboard()
        return keyboard


def print_menu(user, state):
    keyboard = Create_board(state)
    vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
                                             'message': config.get('chat').get(state).get('intro'),
                                             'random_id': 0, 'keyboard': keyboard})


# def print_object(user, state):
#     chat = 'chat'
#     keyboard = Create_board(state)
#     vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
#                                              'message': config.get(chat).get(state).get('intro'),
#                                              'random_id': 0, 'keyboard': keyboard})



#
# def print_abitur(user):
#     state = '/abitur'
#     chat = 'chat'
#     keyboard = Create_board(state)
#     # vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
#     #                                          'message': config.get(chat).get(state).get('intro') +
#     #                                                     config.get(chat).get(state).get('item1') +
#     #                                                     config.get(chat).get(state).get('item2') +
#     #                                                     config.get(chat).get(state).get('item3') +
#     #                                                     config.get(chat).get(state).get('item4'),
#     #                                          'random_id': 0, 'keyboard': keyboard})
#     vk_sessionGroup.method('messages.send', {'user_id': user['user_id'],
#                                              'message': 'Клавиатура',
#                                              'random_id': 0, 'keyboard': keyboard})
