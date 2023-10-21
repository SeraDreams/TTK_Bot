from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re


class FindPassportData:
    def __init__(self, filepath: str):
        self.filepath = self.check_filepath(filepath)
        self.model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)
        self.doc = DocumentFile.from_images(self.filepath)

    def start(self) -> dict:
        try:
            res = self.model(self.doc)
            down_line = re.sub(r"[\D]", "", res.pages[0].blocks[-1].lines[-1].words[0].value)
            nomer = down_line[:3] + down_line[17]
            seria = down_line[3:9]
            data = {"nomer": nomer, "seria": seria}

            return data
        except Exception as e:
            raise e

    @staticmethod
    def check_filepath(f):
        if not isinstance(f, str):
            raise TypeError("filepath is not str")
        return f


if __name__ == "__main__":
    filepath = 'passport_img/img.png'
    print(FindPassportData(filepath=filepath).start())
