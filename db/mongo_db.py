from pymongo import MongoClient
from events.vkbot_auth import vk_sessionGroup, id_group
from read_json import get_json
from bson.binary import Binary
import pickle

__host = get_json('config\\credentials').get('mongo_client').get('host')
__port = get_json('config\\credentials').get('mongo_client').get('port')
__client = MongoClient(__host, __port)

albums = __client[f'public{id_group}']['album_photos']
users = __client[f'public{id_group}']['users']


def clean_collection(collection):
    collection.delete_many({})


def set_user_state(collection, user, state):
    user_id = user['user_id']
    collection.update_one({'user_id': user_id},
                          {
                              '$set':
                                  {
                                      'chat':
                                          {
                                              'state': state
                                          }
                                  }
                          })



def insert_user(collection, event):
    user_id = event.object['message']['from_id']
    user = vk_sessionGroup.method("users.get", {'user_ids': user_id})
    collection.insert_one(
        {
            "user_id": user_id,
            "first_name": user[0]['first_name'],
            "last_name": user[0]['last_name'],
            "chat": {
                "state": None,
            }
        })


def find_images(collection):
    filter_obj = {'count': {'$exists': False}}
    images_list = []
    for image in collection.find(filter_obj):
        for index in range(len(image['objects']['faces'])):
            image['objects']['faces'][index]['emb'] = pickle.loads(image['objects']['faces'][index]['emb'])
        images_list.append(image)
    return images_list


def insert_photo(collection, image):
    count_faces = len(image['objects'])
    collection.insert_one(
        {
            "localhost": {
                "name": image['img_name'],
                "path": image['path']
            },

            "objects":
                {
                    "count": count_faces,
                    "faces": []
                }
        })
    """
        "vkserver":
            {
                "album_id": image['vk'][0]['album_id'],
                "date": image['vk'][0]['date'],
                "id": image['vk'][0]['id'],
                "owner_id": image['vk'][0]['owner_id'],
                "type": image['vk'][0]['sizes'][image['vk'][1]]['type'],
                "url": image['vk'][0]['sizes'][image['vk'][1]]['url']
            },
        "height": image['vk'][0]['sizes'][image['vk'][1]]['height'],
        "width": image['vk'][0]['sizes'][image['vk'][1]]['width'],
    """
    index = 0
    for face in image['objects']:
        if len(face) == 0:
            continue
        face['emb'] = Binary(pickle.dumps(face['emb'], protocol=2), subtype=128)
        collection.update_one({'localhost.name': image['img_name']},
                              {
                                  '$set':
                                      {
                                          f'objects.faces.{index}':
                                              {
                                                  'emb': face['emb'],
                                                  'loc': [int(k) for k in face['loc'][0]],
                                                  'face_path': face['face_path'],
                                                  'image_path': face['image_path']
                                              }
                                      }
                              })
        index += 1
