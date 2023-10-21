import os

from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re


class FindTicketData:
    def __init__(self, filepath: str):
        self.filepath = self.check_filepath(filepath)
        self.model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)
        self.doc = DocumentFile.from_images(self.filepath)

    def start(self) -> str:
        try:
            res = self.model(self.doc)
            for page in res.pages:
                for block in page.blocks:
                    for line in block.lines:
                        num_ticket = ''
                        for word in line.words:
                            num_ticket += str(word.value)
                            if (len(str(word.value)) == 13 or len(str(word.value)) == 14) and str(word.value).isdigit():
                                return str(word.value)
                        num_ticket_clear = re.sub(r'[^\d\.]', '', num_ticket)
                        if (len(num_ticket_clear) == 13 or len(num_ticket_clear) == 14) and num_ticket_clear.isdigit():
                            return num_ticket_clear
        except Exception as e:
            raise e

    @staticmethod
    def check_filepath(f):
        if not isinstance(f, str):
            raise TypeError("filepath is not str")
        return f


if __name__ == "__main__":
    for filename in os.listdir('check_img'):
        filepath = f'check_img/{filename}'
        with open(f'check_result/{filename.split(".")[0]}.txt', 'w') as file:
            file.write(FindTicketData(filepath=filepath).start())
