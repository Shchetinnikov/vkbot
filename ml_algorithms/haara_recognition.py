import numpy as np
from PIL import Image
import cv2
import face_recognition
from read_json import get_json


cascadePath = 'ml_algorithms\\haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer = cv2.face.LBPHFaceRecognizer_create(1, 8, 8, 8, 123)

config = get_json('config\\config')
id_group = get_json('config\\credentials').get('group').get('id_group')

MAX_DISTANCE = 0.6


# Сравниваем данные лиц
def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=MAX_DISTANCE):
    return face_recognition.compare_faces(known_face_encodings, face_encoding_to_check, tolerance=MAX_DISTANCE)

    # code = False
    # for index in range(len(image_data)):
    #
    #     distance = face_recognition.face_distance(victim_data[0]['emb'], image_data[index]['embedding'])
    #     print("Picture: ", image_data[index]['image_path'].split('\\')[-1], "   Distance: ", distance, end='')
    #     if np.any(distance <= MAX_DISTANCE):
    #         sus = Image.open(image_data[index]['face_path'])
    #         Image.Image.save(sus, f'{config.get("media_folder").get("name")}\\{id_group}\\'
    #                               f'{config.get("media_folder").get("folders").get("public").get("suspected")}\\' + image_data[index]['face_path'].split('\\')[-1])
    #         Image.Image.close(sus)
    #         print("  <suspected>", end='')
    #         code = True
    #     print()
    # return code


# Получаем данные лиц с фотографии
def get_faces(image_path):
    image_name = image_path.split('\\')[-1].split('.jpg')[0]
    image = Image.open(image_path)
    gray = image.convert('L')
    gray_arr = np.array(gray, 'uint8')

    # Получение локации лиц (список локаций)
    faces = faceCascade.detectMultiScale(gray_arr, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    faces_data = []
    for x, y, w, h in faces:
        face_data = {}
        locations = [(y, x + w, y + h, x)]

        # Сохранение лица в папку
        # cropped = Image.Image.crop(image, (x, y, x + w, y + h))
        # cropped.save(rf"{config.get('media_folder').get('name')}\\{id_group}"
        #              rf"\\{config.get('media_folder').get('folders').get('public').get('faces')}\\" + image_name + f"_{face_index}.jpg")

        # Получаем вложения (спосок вложений)
        image_rgb = image.convert('RGB')
        image_arr = np.array(image_rgb, 'uint8')
        face_encodings = face_recognition.face_encodings(image_arr, locations)

        print(face_encodings)

        # face_data['face_path'] = f"{config.get('media_folder').get('name')}\\{id_group}" \
        #                          f"\\{config.get('media_folder').get('folders').get('public').get('faces')}\\" + image_name + f"_{face_index}.jpg"
        face_data['image_path'] = image_path
        face_data['loc'] = locations
        face_data['emb'] = face_encodings[0]

        faces_data.append(face_data)

    Image.Image.close(image)
    return faces_data
