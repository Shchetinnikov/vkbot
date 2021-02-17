import os
import uuid
import requests
from zipfile import ZipFile

from db import mongo_db as mdb
from events.vkbot_auth import config, id_group, vk_sessionUser
from ml_algorithms import model_learning
from ml_algorithms.haara_recognition import get_faces, compare_faces
from exceptions.user_exceptions import *


# Скачивает изображение, генерирует уникальное имя
def download_photo(url, path):
    print("Running the function: ", download_photo.__name__)

    name = uuid.uuid4()
    img_name = f'{name}.jpg'
    img_data = requests.get(url).content
    with open(path + img_name, 'wb') as photo:
        photo.write(img_data)

    print(download_photo.__name__, " function is completed", end='\n\n')
    return img_name


# Создает архив изображений
def create_images_archive(person_photos):
    print("Running the function: ", create_images_archive.__name__)

    if len(person_photos) == 0:
        raise NotFoundError(config.get('chat').get('errors').get('photo').get('not_found'))

    path = f"{config.get('media_folder').get('name')}\\{id_group}\\" \
           f"{config.get('media_folder').get('folders').get('public').get('archives')}\\"
    name = uuid.uuid4()
    archive_name = f"{name}.zip"

    with ZipFile(path + archive_name, "w") as newzip:
        for photo in person_photos:
            im_path = photo["localhost"]["path"]
            im_name = photo["localhost"]["name"]
            newzip.write(im_path + im_name)

    print(create_images_archive.__name__, " function is completed", end='\n\n')
    return path, archive_name


# Создает объект изображения
def create_image_obj(path, url):
    print("Running the function: ", create_image_obj.__name__)

    # Скачивает изображение, возвращает уникальное имя
    img_name = download_photo(url, path)

    image = {}
    faces_data = get_faces(path + img_name)
    image['objects'] = faces_data
    image['img_name'] = img_name
    image['path'] = path
    image['url'] = url

    print(create_image_obj.__name__, " function is completed", end='\n\n')
    return image


# Удаление архива из хранилища
def delete_archive(path, archive_name):
    print("Running the function: ", delete_archive.__name__)

    for file in os.listdir(path):
        if file == archive_name:
            archive_path = os.path.join(path, file)
            os.remove(archive_path)

    print(delete_archive.__name__, " function is completed")
    return


# Удаление фотографии из хранилища
def delete_photo(path, image_name):
    print("Running the function: ", delete_photo.__name__)

    # image_formats = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'raw', 'pcx', 'tga']
    for file in os.listdir(path):
        if file == image_name:
            image_path = os.path.join(path, file)
            os.remove(image_path)

    print(delete_photo.__name__, " function is completed")
    return


# Удаление данных об изображении
def delete_photo_data(photo):
    print("Running the function: ", delete_photo_data.__name__)

    # Удаление в хранилище
    delete_photo(photo['localhost']['path'], photo['localhost']['name'])

    # Удаление фотографии в поле photos_id пользователей
    # users_id = set()
    # emb_list = mdb.get_embeddings_by_filter({"photo_id": photo['_id']})
    #
    # # Определяем пользователей
    # for emb in emb_list:
    #     if emb['user_id'] is not None:
    #         users_id.add(emb['user_id'])
    #
    # for user_id in users_id:
    #     current_photos_id = mdb.get_user_photos(user_id)
    #     current_photos_id.remove(photo['_id'])
    #     mdb.update_user_photos(user_id, current_photos_id)

    # Удаление лиц фотографии из коллекции embeddings
    mdb.delete_embeddings_by_filter({"photo_id": photo['_id']})

    # Удаление фотографии из коллекции photos
    mdb.delete_photo(photo)

    print(delete_photo_data.__name__, " function is completed")
    return


# Получить все url-адреса фотографий сообщества
def get_album_photos_url():
    print("Running the function: ", get_album_photos_url.__name__)

    url_list = []
    offset = 0

    while True:
        photos = vk_sessionUser.method('photos.getAll', {'owner_id': -id_group, 'offset': offset,
                                                         'count': 200, 'photo_sizes': 0, 'no_service_albums': 0})
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

    print(get_album_photos_url.__name__, " function is completed", end='\n\n')
    return url_list


# Возвращает списки url-адресов новых и объекты удаленных фотографий
def _get_data_diffs(url_list):
    print("Running the function: ", _get_data_diffs.__name__)

    added_list = []
    deleted_list = []

    if not mdb.photos_clt.count():
        added_list = url_list
    else:
        db_photos = mdb.get_photos()

        # Проверка на новые фотографии
        for url in url_list:
            flag = False
            for photo in db_photos:
                if url == photo['url']:
                    flag = True
                    break
            if not flag:
                added_list.append(url)

        # Проверка на удаленные фотографии
        for photo in db_photos:
            flag = False
            for url in url_list:
                if url == photo['url']:
                    flag = True
                    break
            if not flag:
                deleted_list.append(photo)

    print(_get_data_diffs.__name__, " function is completed", end='\n\n')
    return added_list, deleted_list


# Обновление базы фотографий сообщества
def update_data():
    print("Running the function: ", update_data.__name__)

    # Получить списки url-адресов новых фотографий и объекты удаленных фотографий
    url_list = get_album_photos_url()
    added_list, deleted_list = _get_data_diffs(url_list)

    # Очистить данные об удаленных фотографиях
    for photo in deleted_list:
        delete_photo_data(photo)

    emb_list = []  # новый список embeddings

    # Добавление новых фотографий на сервер, получение embeddings
    new_photos = []
    for url in added_list:
        path = f"{config.get('media_folder').get('name')}\\{id_group}\\" \
               f"{config.get('media_folder').get('folders').get('public').get('albums')}\\"
        image = create_image_obj(path, url)
        new_photos.append(image)

        for face_data in image['objects']:
            emb_list.append(face_data['emb'])

    faces_count = len(emb_list)  # запомнили кол-во первых(новых) embeddings

    # Дополняем новый список embeddings данными из БД
    # Соответственно, запоминаем принадлежность к классу
    # current_users_id = []   # соответствующие значения поля user_id
    emb_id_list = []
    current_labels = []     # текущие известные классы
    for embedding in mdb.get_embeddings():
        emb_id_list.append(embedding['_id'])
        emb_list.append(embedding['embedding'])
        current_labels.append(embedding['cluster'])
        # current_users_id.append(embedding['user_id'])

    # Кластеризация embeddings
    pairs = {}              # взаимно-однозначное соответвие новых и старых значений кластеров
    new_labels = []         # обучащие метки
    clusters = set()        # новые кластеры, присвоенные известным фотографиям
    new_photos_labels = []  # кластеры новых фотографий

    # Проверка на необходимость кластеризации
    if len(added_list) != 0:
        components, new_labels_np = model_learning.clustering(emb_list)

        # Преобразование типа np.int64 кластера к int
        for i in range(len(new_labels_np)):
            new_labels.append(new_labels_np[i].item())

        # Замена новых значений кластеров для известных фото старыми значениями из БД
        # for i in range(faces_count, len(new_labels)):
        #     pairs[new_labels[i]] = []
        # for i in range(faces_count, len(new_labels)):
        #     # pairs[new_labels[i]].append([current_labels[i - faces_count], current_users_id[i - faces_count]])
        #     pairs[new_labels[i]].append(current_labels[i - faces_count])
        #     clusters.add(new_labels[i])
        #     # if current_users_id[i - faces_count]:
        #     #     new_labels[i] = current_users_id[i - faces_count]
        #     # else:
        #     new_labels[i] = current_labels[i - faces_count]

    else:
        for i in range(len(current_labels)):
            # if current_users_id[i]:
            #     new_labels.append(current_users_id[i])
            # else:
            new_labels.append(current_labels[i])
        # components = emb_list

    # Определение новых фото в кластеры БД, иначе сохранить новое имя кластера
    # for i in range(faces_count):
    #     if new_labels[i] in clusters:
    #         '''
    #             ПРОБЛЕМА ОБЪЕДИНЕНИЯ КЛАСТЕРОВ
    #         '''
    #         cluster = -1
    #         for cluster in pairs[new_labels[i]]:
    #             member = mdb.get_embedding({'cluster': cluster})
    #             if compare_faces([emb_list[i]], member['embedding'])[0]:
    #                 # if element[1]:
    #                 #     new_labels[i] = element[1]
    #                 # else:
    #                 #     new_labels[i] = element[0]
    #                 new_labels[i] = cluster
    #                 break
    #         new_photos_labels.append(cluster)
    #     else:
    #         new_photos_labels.append(new_labels[i])

    # Обучение классификатора
    if len(emb_list):
        model_learning.fit(emb_list, new_labels)

    # Обновление кластеров embeddings в БД
    mdb.update_embeddings_clusters(emb_id_list, new_labels[faces_count:])

    # Добавление новых данных в базу
    #   - фотографии
    #   - embeddings
    #   - обновление списка фотографий пользователя
    item = 0
    # user_id_photos_pairs = {}
    # for i in range(faces_count):
    #     user_id_photos_pairs[new_labels[i]] = set()

    for photo in new_photos:
        # Добавление фотографии в БД
        photo_id = mdb.insert_photo(photo)

        # Добавление embeddings в БД
        for face_data in photo['objects']:
            # mdb.insert_embedding(face_data['emb'], new_labels[item], new_photos_labels[item], photo_id)
            mdb.insert_embedding(face_data['emb'], new_labels[item], photo_id)
            # user_id_photos_pairs[new_labels[item]].add(photo_id)
            item += 1

    # Обновление списка фотографий пользователя
    # for user_id, photos_id in user_id_photos_pairs.items():
    #     new_photos_id = list(photos_id)
    #     current_photos_id = mdb.get_user_photos(user_id)
    #     if current_photos_id:
    #         mdb.update_user_photos(user_id, new_photos_id + current_photos_id)

    print(update_data.__name__, " function is completed", end='\n\n')
    return
