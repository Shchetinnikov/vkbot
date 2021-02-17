from datetime import datetime
from bson.binary import Binary
import pickle
from pymongo import MongoClient

from timer import time_tools
from events.vkbot_auth import vk_sessionGroup, id_group
from read_json import get_json

__host = get_json('config\\credentials').get('mongo_client').get('host')
__port = get_json('config\\credentials').get('mongo_client').get('port')
__client = MongoClient(__host, __port)

photos_clt = __client[f'public{id_group}']['photos']
users_clt = __client[f'public{id_group}']['users']
emb_clt = __client[f'public{id_group}']['embeddings']


# Работа с пользователями
# def get_user_photos(user_id):
#     user = users_clt.find_one({"user_id": user_id})
#     if user:
#         return user['photos']
#     else:
#         return None


# def get_user_data(user_id):
#     user = users_clt.find_one({"user_id": user_id})
#     if user:
#         if user['embedding'] is not None:
#             user['embedding'] = pickle.loads(user['embedding'])
#     return user


def update_last_greeting(user):
    user_id = user['user_id']
    separate_date = time_tools.separate(datetime.now())
    users_clt.update_one({"user_id": user_id},
                         {
                             "$set":
                                 {
                                     "chat.last_greeting": {
                                         "year": separate_date['year'],
                                         "month": separate_date['month'],
                                         "day": separate_date['day'],
                                         "hour": separate_date['hour'],
                                         "minute": separate_date['minute'],
                                         "second": separate_date['second'],
                                         "microsecond": separate_date['microsecond'],
                                         "tzinfo": separate_date['tzinfo']
                                     }
                                 }
                         })
    return


# def update_user_photos(user_id, photos_id):
#     users_clt.update_one({"user_id": user_id},
#                          {
#                              "$set":
#                                  {
#                                      "photos": photos_id
#                                  }
#                          })
#     return


# def set_user_embedding(user, embedding):
#     embedding = Binary(pickle.dumps(embedding, protocol=2), subtype=128)
#     user_id = user['user_id']
#     users_clt.update_one({"user_id": user_id},
#                          {
#                              "$set":
#                                  {
#                                      "embedding": embedding
#                                  }
#                          })
#     return


# def set_user_identify(user, access):
#     user_id = user['user_id']
#     users_clt.update_one({"user_id": user_id},
#                          {
#                              "$set":
#                                  {
#                                      "identify": access
#                                  }
#                          })
#     return


def set_user_state(user, state):
    user_id = user['user_id']
    users_clt.update_one({"user_id": user_id},
                         {
                             "$set":
                                 {
                                     "chat.state": state
                                 }
                         })
    return


def insert_user(user_id):
    user = vk_sessionGroup.method("users.get", {"user_ids": user_id})
    separate_date = time_tools.separate(datetime.now())
    output = users_clt.insert_one(
        {
            "user_id": user_id,
            "first_name": user[0]['first_name'],
            "last_name": user[0]['last_name'],
            "admin": 0,
            "chat": {
                "state": None,
                "last_greeting": {
                    "year": separate_date['year'],
                    "month": separate_date['month'],
                    "day": separate_date['day'],
                    "hour": separate_date['hour'],
                    "minute": separate_date['minute'],
                    "second": separate_date['second'],
                    "microsecond": separate_date['microsecond'],
                    "tzinfo": separate_date['tzinfo']
                }
            },
            # "identify": None,
            # "embedding": None,
            # "photos": []
        })
    return output.inserted_id


def delete_user(user_id):
    return users_clt.delete_one({'user_id': user_id}).acknowledged

#################################################################


# Работа с фотографиями
def delete_photo_by_filter(user_filter):
    return photos_clt.delete_one(user_filter).acknowledged


def delete_photo(photo):
    return delete_photo_by_filter({"url": photo['url']})


def get_photos_by_filter(user_filter=None):
    photos = []
    for document in photos_clt.find(user_filter):
        photos.append(document)
    return photos


def get_photos():
    return get_photos_by_filter()


def get_photo(user_filter):
    return photos_clt.find_one(user_filter)  # Возвращает объект


def insert_photo(photo):
    output = photos_clt.insert_one(
        {
            "localhost": {
                "name": photo['img_name'],
                "path": photo['path']
            },
            "url": photo['url'],
        })
    return output.inserted_id


#################################################################


# Работа с embeddings
def delete_embeddings_by_filter(user_filter):
    return emb_clt.delete_many(user_filter).acknowledged


def delete_embeddings(user_filter):
    return emb_clt.delete_many(user_filter)


def get_embedding(user_filter=None):
    emb = emb_clt.find_one(user_filter)
    if emb:
        emb['embedding'] = pickle.loads(emb['embedding'])
    return emb


def get_embeddings_by_filter(user_filter=None):
    emb_list = []
    for emb in emb_clt.find(user_filter):
        emb['embedding'] = pickle.loads(emb['embedding'])
        emb_list.append(emb)
    return emb_list


def get_embeddings():
    return get_embeddings_by_filter()


# def insert_embedding(embedding, user_id, cluster, photo_id):
#     embedding = Binary(pickle.dumps(embedding, protocol=2), subtype=128)
#     if user_id == cluster:
#         user_id = None
#     output = emb_clt.insert_one(
#         {
#             "embedding": embedding,
#             "user_id": user_id,
#             "cluster": cluster,
#             "photo_id": photo_id
#         })
#     return output.inserted_id


def insert_embedding(embedding, cluster, photo_id):
    embedding = Binary(pickle.dumps(embedding, protocol=2), subtype=128)
    output = emb_clt.insert_one(
        {
            "embedding": embedding,
            "cluster": cluster,
            "photo_id": photo_id
        })
    return output.inserted_id


def update_embeddings_clusters(emb_id_list, clusters_list):
    for i in range(len(emb_id_list)):
        emb_clt.update({"_id": emb_id_list[i]},
                       {
                           "$set":
                               {
                                   "cluster": clusters_list[i]
                               }
                       })




# def update_embeddings_user_id(emb_id_list, user_id):
#     for emb_id in emb_id_list:
#         emb_clt.update_one({"_id": emb_id},
#                            {
#                                "$set":
#                                    {
#                                        "user_id": user_id
#                                    }
#                            })
#     return

