import os

from vk_api.bot_longpoll import VkBotEventType
from events import vkbot_chat, vkbot_photo
from events.vkbot_auth import longpoll


if __name__ == '__main__':
    print("Starting the program: ", os.path.basename(__file__))

    while True:
        # timer_start = time()

        # Обновление базы данных фотографий сообщества
        vkbot_photo.update_database()

        """
            if vkbot_photo.ControlAlbumPhotos() == 'Incomplete database':
            elif vkbot_photo.ControlAlbumPhotos() == 'Empty database':
                vkbot_photo.GetAllAlbumPhotos()
        """

        for event in longpoll.listen():

            # Обработка сообщений пользователей
            if event.type == VkBotEventType.MESSAGE_NEW:
                vkbot_chat.message_processing(event)

            # Сохранение новых фотографий в альбомах сообщества
            elif event.type == VkBotEventType.PHOTO_NEW:
                vkbot_photo.get_new_photos(event)


            """
                # Еженедельное обновление базы данных
                elif (time() - timer_start) / (3600 * 24) >= 7:
                    break

                #Сохранение фотографий с нового поста сообщества
                if event.type == VkBotEventType.WALL_POST_NEW:
                    VkBot_photos.getWallPhoto(event)
            """