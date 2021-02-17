import os
from time import sleep
from timer.time_tools import timer_start, time
from _datetime import datetime
import requests
import urllib3
import socket

from vk_api.bot_longpoll import VkBotEventType
from events.vkbot_auth import longpoll
from events import vkbot_chat, vkbot_db

if __name__ == '__main__':
    print("Running the program: ", os.path.basename(__file__), end='\n\n')

    # Обновление базы данных фотографий сообщества
    vkbot_db.update_data()

    while True:
        try:
            photo_counter = 0
            for event in longpoll.listen():

                # Обработка сообщений пользователей
                if event.type == VkBotEventType.MESSAGE_NEW:
                    vkbot_chat.message_processing(event)

                # Обновление базы данных
                if event.type == VkBotEventType.PHOTO_NEW:
                    photo_counter += 1
                    if photo_counter >= 20:
                        timer_start = time()
                        vkbot_db.update_data()
                        photo_counter = 0
                elif (time() - timer_start) / 3600 >= 1:
                    timer_start = time()
                    vkbot_db.update_data()
    
        except (requests.exceptions.ReadTimeout, urllib3.exceptions.ReadTimeoutError, socket.timeout,
                ConnectionResetError, urllib3.exceptions.ProtocolError, requests.exceptions.ConnectionError) as error:
            print("Error time: ", datetime.now(), ", Message: ", error)
