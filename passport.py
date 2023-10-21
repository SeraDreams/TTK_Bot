from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re
import os


class FindPassportData:
    def __init__(self, filepath: str):
        self.filepath = self.check_filepath(filepath)
        self.model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)
        self.doc = DocumentFile.from_images(self.filepath)

    def start(self) -> str:
        res = self.model(self.doc)
        print(self.filepath)
        print(res)
        print('\n\n\n', '+' * 100, '\n\n\n')
        try:
            down_line = re.sub(r"[\D]", "", res.pages[0].blocks[-1].lines[-1].words[0].value)
            number = down_line[:3] + down_line[17]
            seria = down_line[3:9]
            data = str(number) + ' ' + str(seria)

            return data
        except Exception as e:
            return str(e)


    @staticmethod
    def check_filepath(f):
        if not isinstance(f, str):
            raise TypeError("filepath is not str")
        return f


if __name__ == "__main__":
    for filename in os.listdir('passport_img'):
        filepath = f'passport_img/{filename}'
        with open(f'passport_result/{filename.split(".")[0]}.txt', 'w') as file:
            file.write(FindPassportData(filepath=filepath).start())
