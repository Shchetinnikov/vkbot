import os
import uuid

import requests

from db import mongo_db as mdb
from haara_recognition import get_faces, compare_faces
from events.vkbot_auth import config, id_group, vk_sessionUser, vk_sessionGroup, upload
from exceptions.user_exceptions import *


# Скачивает изображение, генерирует уникальное имя
def download_photo(url, path):
    print("Starting the function: ", download_photo.__name__)

    name = uuid.uuid4()
    img_name = f'{name}.jpg'
    img_data = requests.get(url).content
    with open(path + img_name, 'wb') as photo:
        photo.write(img_data)

    print(download_photo.__name__, " function is completed")
    return img_name


# Удаление фотографий их хранилища
def clean_storage(path):
    print("Starting the function: ", clean_storage.__name__)

    image_formats = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'raw', 'pcx', 'tga']
    for file in os.listdir(path):
        if file.split('.')[-1] in image_formats:
            image_path = os.path.join(path, file)
            os.remove(image_path)

    print(clean_storage.__name__, " function is completed")
    return


# Создает объект изображения
def create_image_obj(img_name, path):
    print("Starting the function: ", create_image_obj.__name__)

    image = {}
    faces_data = get_faces(path + img_name)
    image['objects'] = faces_data
    image['img_name'] = img_name
    image['path'] = path
    """
        image['vk'] = images_list[item]
    """

    print(create_image_obj.__name__, " function is completed")
    return image


# Оправляет пользователю фотографии с данным человеком
def send_photos_to_user(person_photos, event):
    print("Starting the function: ", send_photos_to_user.__name__)

    if len(person_photos) == 0:
        raise NotFoundError(config.get('chat').get('errors').get('photo').get('not_found'))

    attachments = []
    counter = 0
    for image in person_photos:
        if counter == 10:
            vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'], 'random_id': 0,
                                                     'attachment': ','.join(attachments)})
            attachments = []
            counter = 1
            message = upload.photo_messages(image['localhost']['path'] + image['localhost']['name'])[0]
            attachments.append('photo{}_{}'.format(message['owner_id'], message['id']))
        else:
            counter += 1
            message = upload.photo_messages(image['localhost']['path'] + image['localhost']['name'])[0]
            attachments.append('photo{}_{}'.format(message['owner_id'], message['id']))
    if counter:
        vk_sessionGroup.method('messages.send', {'user_id': event.object['message']['from_id'], 'random_id': 0,
                                                 'attachment': ','.join(attachments)})

    print(send_photos_to_user.__name__, " function is completed")
    return


# Находит фотографии с данным человеком
def search_person(face_data):
    print("Starting the function: ", search_person.__name__)

    if len(face_data) != 1:
        raise FaceDataError(config.get('chat').get('errors').get('photo').get('face_data'))

    person_photos = []
    images_list = mdb.find_images(mdb.albums)
    for image in images_list:
        if image['objects']['count'] != 0:
            if compare_faces(face_data, image['objects']['faces']):
                person_photos.append(image)

    if len(person_photos) == 0:
        raise NotFoundError(config.get('chat').get('errors').get('photo').get('not_found'))

    print(search_person.__name__, " function is completed")
    return person_photos


# Скачивает фотографию пользователя
def get_user_photo(event):
    print("Starting the function: ", get_user_photo.__name__)

    if len(event.object['message']['attachments']) == 1 and event.object['message']['attachments'][0]["type"] == 'photo':

        # Выбор разрешения изображения
        url = None
        code = False
        for type_index in range(len(config.get('photo_sizes'))):
            for size_ind in range(len(event.object['message']['attachments'][0]['photo']['sizes'])):
                if event.object['message']['attachments'][0]['photo']['sizes'][size_ind]['type'] == \
                        config.get('photo_sizes')[type_index]:
                    url = event.object['message']['attachments'][0]['photo']['sizes'][size_ind]['url']
                    code = True
                    break
            if code:
                break
        if not code:
            raise InvalidPhotoError(config.get('chat').get('errors').get('photo').get('size'))

        # Сохранение в хранилище
        path = f'{config.get("media_folder").get("name")}\\{id_group}\\' \
               f'{config.get("media_folder").get("folders").get("public").get("users")}\\'
        img_name = download_photo(url, path)

        # Получение данных изображения
        face_data = get_faces(path + img_name)
        if len(face_data) != 1:
            raise InvalidPhotoError(config.get('chat').get('errors').get('photo').get('one_person'))
        """
            image = {}
            image['vk'] = image_list
            image['objects'] = faces_data
            image['img_name'] = img_name
            image['path'] = path
        """

        print(get_user_photo.__name__, " function is completed")
        return face_data

    else:
        raise PhotoCountError(config.get('chat').get('errors').get('photo').get('one_person'))


# Установка фотографий сообщества на сервер
def get_albums_photos():
    print("Starting the function: ", get_albums_photos.__name__)

    url_list = []
    offset = 0

    while True:
        photos = vk_sessionUser.method('photos.getAll',
                                       {'owner_id': -id_group, 'offset': offset, 'count': 200, 'photo_sizes': 0,
                                        'no_service_albums': 0})
        # Выбор разрешений изображений
        for image in photos['items']:
            code = False
            for type_index in range(len(config.get('photo_sizes'))):
                for size_ind in range(len(image['sizes'])):
                    if image['sizes'][size_ind]['type'] == config.get('photo_sizes')[type_index]:
                        url_list.append(image['sizes'][size_ind]['url'])
                        code = True
                        break
                if code:
                    break
        if len(photos['items']) != 200:
            break
        else:
            offset += 200

    # Сохранение в хранилище
    for url in url_list:
        path = f"{config.get('media_folder').get('name')}\\{id_group}\\"
        img_name = download_photo(url, path)

        # Добавление в базу
        image = create_image_obj(img_name, path)
        mdb.insert_photo(mdb.albums, image)

    print(get_albums_photos.__name__, " function is completed")
    return


# Скачивает новые фотографии и добавляет в БД
def get_new_photos(event):
    print("Starting the function: ", get_new_photos.__name__)

    image_list = []

    # Выбор разрешения изображения
    url = None
    code = False
    for type_index in range(len(config.get('photo_sizes'))):
        for size_ind in range(len(event.object['sizes'])):
            if event.object['sizes'][size_ind]['type'] == config.get('photo_sizes')[type_index]:
                url = event.object['sizes'][size_ind]['url']
                code = True
                break
        if code:
            break

    if not code:
        return

    # Сохранение в хранилище
    path = f"{config.get('media_folder').get('name')}\\{id_group}\\{config.get('media_folder').get('folders').get('public').get('albums')}"
    img_name = download_photo(url, path)

    # Добавление в базу
    image = create_image_obj(img_name, path)
    mdb.insert_photo(mdb.albums, image)

    print(get_new_photos.__name__, " function is completed")
    return


# Обновление базы данных
def update_database():
    print("Starting the function: ", update_database.__name__)

    # Удаление данных фотографий сообщества в базе и хранилище
    path = f"{config.get('media_folder').get('name')}\\{id_group}\\" \
           f"{config.get('media_folder').get('folders').get('public').get('albums')}"
    clean_storage(path)
    mdb.clean_collection(mdb.albums)


    # Установка фотографий сообщества на сервер
    get_albums_photos()

    print(update_database.__name__, " function is completed")
    return



"""
    Сохраняет фотографии с нового поста сообщества
    def getWallPhoto(event):
        img_data = 0
        for i in range(len(event.object['attachments'])):
            if event.object['attachments'][i]['type'] == 'photo':
                code = False
                for j in range(len(config.get('photo_sizes'))):
                    for k in range(len(event.object['attachments'][i]['photo']['sizes'])):
                        if event.object['attachments'][i]['photo']['sizes'][k]['type'] == config.get('photo_sizes')[j]:
                            img_data = requests.get(event.object['attachments'][i]['photo']['sizes'][k]['url']).content
                            code = True
                            break
                    if code:
                        break
                if code == False:
                    continue
                id = uuid.uuid4()
                name_img = f'{id}.jpg'
                with open(f'{config.get("media_folder").get("name")}/{id_group}/' + name_img, 'wb') as photo:
                    photo.write(img_data)
                print(event.object)
            else:
                break


    Скачивает все фотографии сообщества и добавляет в БД
    def GetAllAlbumPhotos():
        count = 0
        images_list = []
        offset = 0

        while True:
            photos = vk_sessionUser.method('photos.getAll',
                                   {'owner_id': -id_group, 'offset': offset, 'count': 200, 'photo_sizes': 0,
                                    'no_service_albums': 0})
            for image in photos['items']:
                code = False
                for type_index in range(len(config.get('photo_sizes'))):
                    for size_ind in range(len(image['sizes'])):
                        if image['sizes'][size_ind]['type'] == config.get('photo_sizes')[type_index]:
                            images_list.append([image, size_ind])
                            count += 1
                            code = True
                            break
                    if code:
                        break
            if len(photos['items']) != 200:
                break
            else:
                offset += 200

        mdb.Add_data(album_photos, {"count": count})
        for item in range(count):
            name = uuid.uuid4()
            img_name = f'{name}.jpg'
            path = f'{config.get("media_folder").get("name")}\\{id_group}\\'
            img_data = requests.get(images_list[item][0]['sizes'][images_list[item][1]]['url']).content
            with open(path + img_name, 'wb') as photo:
                photo.write(img_data)

            image = {}
            faces_data = get_faces(path + img_name)
            image['vk'] = images_list[item]
            image['objects'] = faces_data
            image['img_name'] = img_name
            image['path'] = path
            mdb.Add_photo(album_photos, image)
        print('"AlbumPhoto" downloading is completed')

    def GetPhotosCount():
        count = 0
        offset = 0
        while True:
            photos = vk_sessionUser.method('photos.getAll',
                                       {'owner_id': -id_group, 'offset': offset, 'count': 200, 'photo_sizes': 0,
                                        'no_service_albums': 0})
            count += len(photos['items'])
            if len(photos['items']) != 200:
                break
            else:
                offset += 200
        print('Album Photos are counted')
        return count
    
    
    Проверка изменений фотографий в сообществе через БД
    def ControlAlbumPhotos():
        # Проверка изменений в БД
        if album_photos.count() == 0:
            return 'Empty database'
        else:
            return 'Incomplete database'
"""
