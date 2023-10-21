import os

import pytesseract
import cv2
import re


def text_recognising(file_path, text_file_name):
    result = pytesseract.image_to_string(file_path, nice=3, config='--oem 3 --psm 6', lang='eng+rus')
    with open(f'check_result/{text_file_name}', 'w') as file:
        for line in result:
            file.write(f'{line}')

    with open(f'check_result_clear/{text_file_name}', "w") as file:
        pattern = r"(?:\d\s?){14}"
        matches = re.findall(pattern, result)
        num = re.sub('\s', '', matches[0]) if matches else None
        file.write(f'Ticket №{num}')
        print(f'Ticket №{num}')

    return f"Result wrote into {text_file_name}\n{'+' * 40}"


def file_loader():
    for file_name in os.listdir('check_img'):
        file_path = f'check_img/{file_name}'
        img = cv2.imread(file_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print(text_recognising(file_path=img, text_file_name=f'result_{file_name.split(".")[0]}'))


if __name__ == "__main__":
    file_loader()
