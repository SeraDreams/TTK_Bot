import re

from doctr.models import ocr_predictor
from doctr.io import DocumentFile


class FindTicketData:
    def __init__(self, filepath: str):
        # Устанавливаем путь к файлу
        self.filepath = self.check_filepath(filepath)
        # Инициализируем модель для распознавания
        self.model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)
        # Создаем объект документа из изображений, указанных в filepath
        self.doc = DocumentFile.from_images(self.filepath)

    def start(self) -> str:
        try:
            # Запуск модели для распознавания текста на фото
            res = self.model(self.doc)
            # Перебор словаря с поиском номера билета по условию
            for page in res.pages:
                for block in page.blocks:
                    for line in block.lines:
                        num_ticket = ''
                        for word in line.words:
                            # Если весь номер билета содержится в одной ячейке, то мы возвращаем ответ пользователю
                            if (len(str(word.value)) == 13 or len(str(word.value)) == 14) and str(word.value).isdigit():
                                return str(word.value)
                            # Если нет, то мы прибавляем его к будущем номеру тикета
                            num_ticket += str(word.value)
                        # Убираем у билета символы по типу "№" или " "
                        num_ticket_clear = re.sub(r'[^\d\.]', '', num_ticket)
                        # Проверка содержит ли num_ticket_clear номер билета
                        if (len(num_ticket_clear) == 13 or len(num_ticket_clear) == 14) and num_ticket_clear.isdigit():
                            return num_ticket_clear
        except:
            return 'Не удалось распознать номер билета, пожалуйста отправьте фото повторно или введите номер вручную'

    @staticmethod
    def check_filepath(f):
        if not isinstance(f, str):
            raise TypeError("filepath is not str")
        return f


# if __name__ == "__main__":
#     # Чтение файлов из директории check_img
#     # for filename in os.listdir('check_img'):
#     #     # Создание пути до файла в директории
#     #     filepath = f'check_img/{filename}'
#     #     # Создание отчёт файла и помещение его в директорию check_result
#     #     with open(f'check_result/{filename.split(".")[0]}.txt', 'w') as file:
#     #         # Запись данных в файл с запросом на их получение и передачи пути для обрабатываемого файла
#     #         file.write(FindTicketData(filepath=filepath).start())
