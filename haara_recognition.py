import numpy as np
from PIL import Image
import cv2, os
import face_recognition
from read_json import get_json


cascadePath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer = cv2.face.LBPHFaceRecognizer_create(1, 8, 8, 8, 123)

config = get_json('config')
id_group = get_json('credentials').get('group').get('id_group')

MAX_DISTANCE = 0.6

def compare_faces(victim_data, image_data):
    code = False
    for index in range(len(image_data)):
        distance = face_recognition.face_distance(victim_data[0]['emb'], image_data[index]['emb'][0])
        print("Picture: ", image_data[index]['image_path'].split('\\')[-1], "   Distance: ", distance, end='')
        if np.any(distance <= MAX_DISTANCE):
            sus = Image.open(image_data[index]['face_path'])
            Image.Image.save(sus, f'{config.get("media_folder").get("name")}\\{id_group}\\'
                                  f'{config.get("media_folder").get("folders").get("public").get("suspected")}\\' + image_data[index]['face_path'].split('\\')[-1])
            Image.Image.close(sus)
            print("  <suspected>", end='')
            code = True
        print()
    return code

def get_faces(image_path):
    """
     if len(face_data) != 1:
                return "Warning"
            else:
    :param image_path:
    :return:
    """
    image_name = image_path.split('\\')[-1].split('.jpg')[0]
    image = Image.open(image_path)
    gray = image.convert('L')
    gray_arr = np.array(gray, 'uint8')

    # Получение локации лиц (список списков)
    faces = faceCascade.detectMultiScale(gray_arr, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    faces_data = []
    face_index = 0
    for x, y, w, h in faces:
        face_data = {}
        location = [(y, x + w, y + h, x)]

        # Сохранение лица в папку
        cropped = Image.Image.crop(image, (x, y, x + w, y + h))
        cropped.save(rf"{config.get('media_folder').get('name')}\\{id_group}"
                     rf"\\{config.get('media_folder').get('folders').get('public').get('faces')}\\" + image_name + f"_{face_index}.jpg")

        # Получаем вложения
        image_rgb = image.convert('RGB')
        image_arr = np.array(image_rgb)
        face_encodings = face_recognition.face_encodings(image_arr, location)
        print(face_encodings)

        face_data['emb'] = face_encodings
        face_data['loc'] = location
        face_data['face_path'] = f"{config.get('media_folder').get('name')}\\{id_group}" \
                                 f"\\{config.get('media_folder').get('folders').get('public').get('faces')}\\" + image_name + f"_{face_index}.jpg"
        face_data['image_path'] = image_path
        face_index += 1
        faces_data.append(face_data)
    Image.Image.close(image)
    return faces_data

if __name__ == '__main__':

    print("Starting the program 'haara_recognition'")

    # # Тестовое изображение(шаблон), находим лица и создаем вложения
    # image_path = "victim/test.jpg"
    # print("Getting data of test image...")
    # victim_data = get_faces(image_path)
    #
    # # Формируем список изображений, с которыми будем сравнивать шаблон
    # image_paths = [os.path.join("test_me/", f) for f in os.listdir("test_me/")]
    #
    #
    # # Проходим по списку изображений, находим лица и создаем вложения
    # print("Getting data of base images...")
    # for image_path in image_paths:
    #     image_data = get_faces(image_path)
    #     # Сравниваем шаблон со списком изображений
    #     print("Start image comparison...")
    #     compare_faces(victim_data, image_data)
    # print("Base images are applied.", end ="\n\n")
    #
    # print("End of face recognition.")
