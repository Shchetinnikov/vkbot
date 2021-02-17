import random
import numpy as np

from db import mongo_db as mdb
from events.interface.interface import Create_board
from events.vkbot_auth import config, id_group, vk_sessionGroup, upload
from events.vkbot_db import download_photo, create_images_archive, delete_archive
from ml_algorithms import model_learning
from ml_algorithms.haara_recognition import get_faces, compare_faces
from exceptions.user_exceptions import *


# Отправляет образец фотографии
def send_example(user_id, state):
    print("Running the function: ", send_example.__name__)

    attachments = []
    keyboard = Create_board(state)

    vk_sessionGroup.method('messages.send', {'user_id': user_id,
                                             'message': config.get('chat').get('errors').get('photo').get('one_person'),
                                             'random_id': 0, 'keyboard': keyboard})
    message = upload.photo_messages(f'{config.get("media_folder").get("name")}\\' +
                                    f'{config.get("media_folder").get("folders").get("photo_example")}\\' +
                                    'example.jpg')[0]
    attachments.append('photo{}_{}'.format(message['owner_id'], message['id']))
    vk_sessionGroup.method('messages.send', {'user_id': user_id,
                                             'message': 'Образец:', 'random_id': 0,
                                             'attachment': ','.join(attachments)})
    print(send_example.__name__, " function is completed", end='\n\n')
    return


# Отправляет пользователю архив фотографий с данным человеком
def send_archive_to_user(person_photos, user_id):
    print("Running the function: ", send_archive_to_user.__name__)

    ii16 = np.iinfo(np.int16)

    path, archive_name = create_images_archive(person_photos)

    attachments = []
    document = upload.document_message(path + archive_name, title=f"photos{id_group}", peer_id=user_id)
    attachments.append('doc{}_{}'.format(document['doc']['owner_id'], document['doc']['id']))
    vk_sessionGroup.method('messages.send', {'user_id': user_id,
                                             'random_id': user_id * 10 * ii16.bits + random.randint(0, ii16.max),
                                            'attachment': ','.join(attachments)})

    delete_archive(path, archive_name)
    print(send_archive_to_user.__name__, " function is completed", end='\n\n')
    return


# Оправляет пользователю фотографии с данным человеком
# def send_photos_to_user(person_photos, user_id):
#     print("Running the function: ", send_photos_to_user.__name__)
#
#     if len(person_photos) == 0:
#         raise NotFoundError(config.get('chat').get('errors').get('photo').get('not_found'))
#
#     attachments = []
#     counter = 0
#     ii16 = np.iinfo(np.int16)
#
#     for image in photo_generator(person_photos):
#         path = image['localhost']['path']
#         image_name = image['localhost']['name']
#
#         if counter == 10:
#             ii16 = np.iinfo(np.int16)
#             vk_sessionGroup.method('messages.send', {'user_id': user_id,
#                                                      'random_id': user_id * 10 * ii16.bits + random.randint(0, ii16.max),
#                                                      'attachment': ','.join(attachments)})
#
#             attachments = []
#             counter = 1
#
#             message = upload.photo_messages(path + image_name)[0]
#             attachments.append('photo{}_{}'.format(message['owner_id'], message['id']))
#         else:
#             counter += 1
#
#             message = upload.photo_messages(path + image_name)[0]
#             attachments.append('photo{}_{}'.format(message['owner_id'], message['id']))
#
#     if counter:
#         vk_sessionGroup.method('messages.send', {'user_id': user_id,
#                                                  'random_id': user_id * 10 * ii16.bits + random.randint(0, ii16.max),
#                                                  'attachment': ','.join(attachments)})
#
#     print(send_photos_to_user.__name__, " function is completed", end='\n\n')
#     return


# Найти фотографии с данным человеком
def search_person(user_id, face_data):
    print("Running the function: ", search_person.__name__)

    if len(face_data) != 1:
        raise FaceDataError(config.get('chat').get('errors').get('photo').get('face_data'))

    # Определяем класс
    '''
           Проверка на обученную модель sklearn.exceptions.NotFittedError
    '''
    cluster = int(model_learning.predict([face_data[0]['emb']])[0])

    # Выборка фотографий
    person_photos = []
    photos_id = set()

    # flag = False

    # if cluster == user_id:
    #     user_data = mdb.get_user_data(cluster)
    #     if user_data['embedding'] is not None and compare_faces([face_data[0]['emb']], user_data['embedding']):
    #         photos_id = mdb.get_user_photos(user_id)
    #     else:
    #         flag = True
    # if (cluster != user_id or flag) and cluster != -1:
    # Значение кластера соответствует id другого пользователя, иначе
    # натуральное значение кластера
    '''
            Если идентификация сменилась, но обучение уже прошло, то 
            как быть с классами id, они теперь ничьи
            Последствия изменения данных пользователя и времени переобучения
    '''
    if cluster != -1:

        # user_data = mdb.get_user_data(cluster)
        # if user_data:
        #     if user_data['embedding'] is not None and compare_faces([face_data[0]['emb']], user_data['embedding']):
        #         photos_id = mdb.get_user_photos(cluster)
        #
        # else:
        emb_id_list = []
        member = mdb.get_embedding({"cluster": cluster})

        # Сравниваем с одним лицом данного кластера
        if compare_faces([face_data[0]['emb']], member['embedding'])[0]:
            # user_data = mdb.get_user_data(user_id)
            # if user_data['embedding'] is not None and compare_faces([face_data[0]['emb']], user_data['embedding'])[0]:
            #     emb_list = mdb.get_embeddings_by_filter({"cluster": cluster})
            #     for emb in emb_list:
            #         emb_id_list.append(emb['_id'])
            #         photos_id.add(emb['photo_id'])
            #
            #     photos_id = list(photos_id)
            #
            #     mdb.update_user_photos(user_id, photos_id)
            #     mdb.update_embeddings_user_id(emb_id_list, user_id)
            # else:
            emb_list = mdb.get_embeddings_by_filter({"cluster": cluster})
            for emb in emb_list:
                photos_id.add(emb['photo_id'])

    photos_id = list(photos_id)

    for photo_id in photos_id:
        image = mdb.get_photo({"_id": photo_id})
        person_photos.append(image)

    if len(person_photos) == 0:
        raise NotFoundError(config.get('chat').get('errors').get('photo').get('not_found'))

    print(search_person.__name__, " function is completed", end='\n\n')
    return person_photos


# Скачивает фотографию пользователя
def get_user_photo(event):
    print("Running the function: ", get_user_photo.__name__)

    attach_type = event.object['message']['attachments'][0]["type"]
    if len(event.object['message']['attachments']) != 1 and attach_type != 'photo':
        raise PhotoCountError(config.get('chat').get('errors').get('photo').get('one_person'))

    # Выбор разрешения изображения
    url = None
    code = False

    photo_sizes_config = config.get('photo_sizes')
    photo_sizes = event.object['message']['attachments'][0]['photo']['sizes']

    for type_index in range(len(photo_sizes_config)):
        for size_ind in range(len(photo_sizes)):
            if photo_sizes[size_ind]['type'] == photo_sizes_config[type_index]:
                url = photo_sizes[size_ind]['url']
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

    print(get_user_photo.__name__, " function is completed", end='\n\n')
    return face_data
