import os
from ultralytics import YOLO
import easyocr
import shutil
import cv2

reader = easyocr.Reader(['ru'])
model = YOLO("neuron/passport_model.pt")


def recognize_passport(img: str, user_id: str) -> dict:
    model(img, retina_masks=True, save_crop=True, project="file", name=user_id)

    info = [
        # f"file/{user_id}/crops/first/" + os.listdir(f"file/{user_id}/crops/first/")[0],
        # f"file/{user_id}/crops/last/" + os.listdir(f"file/{user_id}/crops/last/")[0],
        # f"file/{user_id}/crops/patron/" + os.listdir(f"file/{user_id}/crops/patron/")[0],
        f"file/{user_id}/crops/num/" + os.listdir(f"file/{user_id}/crops/num/")[0],
        f"file/{user_id}/crops/ser/" + os.listdir(f"file/{user_id}/crops/ser/")[0],
    ]

    img = cv2.imread(info[-1])
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite(info[-1], img)
    img = cv2.imread(info[-2])
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite(info[-2], img)

    data = {
        # "Имя": "".join(reader.readtext(info[0], detail=0)).lower().capitalize(),
        # "Фамилия": "".join(reader.readtext(info[1], detail=0)).lower().capitalize(),
        # "Отчество": "".join(reader.readtext(info[2], detail=0)).lower().capitalize(),
        "Номер": "".join(reader.readtext(info[0], detail=0)).lower(),
        "Серия": "".join(reader.readtext(info[1], detail=0)).lower(),
    }

    shutil.rmtree(f"file/{user_id}")
    return data
