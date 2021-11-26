import re
import json
import os
from tqdm import tqdm
import argparse


class ReadFile:
    """
       Класс File для чтения из текстового файла

       __data : object
       Содержит считанные данные из текстового файла
    """
    __data: object

    def __init__(self, path: str) -> None:
        """
        Инициализация класса ReadFile данными из файла

        :param path: путь до файла, откуда необходимо считать данные
        """
        try:
            if os.path.exists(path):
                self.__data = json.load(open(path, encoding='windows-1251'))
        except OSError:
            print("Файл по данному пути не существует")

    @property
    def data(self):
        """
        Геттер для класса ReadFile
        :return: Возвращает данные, хранящиеся в классе
        """
        return self.__data


class Validator:
    """
    Объект класса Validator хранит данные полей конкретной записи и предоставляет методы проверки каждого из полей
    """
    __email: str
    __height: float
    __inn: str
    __passport_number: str
    __occupation: str
    __work_experience: int
    __academic_degree: str
    __worldview: str
    __address: str

    def __init__(self, email: str, height: float, inn: str, passport_number: str, occupation: str, work_experience: int,
                 academic_degree: str, worldview: str, address: str):
        """
        Инициализирует поля объекта класса Validator переданными параметрами
        """
        self.__email = email
        self.__height = height
        self.__inn = inn
        self.__passport_number = passport_number
        self.__occupation = occupation
        self.__work_experience = work_experience
        self.__academic_degree = academic_degree
        self.__worldview = worldview
        self.__address = address

    def check_email(self):
        """
        Проверка поля email на валидность
        Проверка исключает email'ы содержащие в себе пробелы
        :return: True - email прошел проверку
                 False - email не прошел проверку
        """
        return re.match(r"[\w\.\d-]+@\w+\.\w+", self.__email) is not None

    def check_height(self):
        """
        Проверяет поле height на валидность
        Если поле height > 1м 20 см и меньше 2м 20 см, то данные валидные
        :return: True - height прошел проверку
                 False - height не прошел проверку
        """
        return re.match(r"\-?\d+\.\d+",
                        str(self.__height)) is not None and float(self.__height) >= 1.2 and float(
            self.__height) <= 2.20

    def check_inn(self):
        """
        Проверка inn на валидность
        Если поле inn состоит из 12 цифр в десятичной системе счисления, то запись считается валидной
        :return: True - inn прошел проверку
                 False - inn не прошел проверку
        """
        return re.match(r"\d{12}", str(self.__inn)) is not None

    def check_passport_number(self):
        """
        Проверка поля passport_number на валидность
        Если поле passport_number состоит из 6 цифр в десятичной системе счисления, то запись считается валидной
        :return: True - passport_number прошел проверку
                 False - passport_number не прошел проверку
        """
        return re.match(r"\d{6}$", str(self.__passport_number)) is not None

    def check_occupation(self):
        """
        Проверка поля occupation на валидность
        Если профессия не находится в списке not_valid_occupation, то считается валидной
        :return: True - occupation прошел проверку
                 False - occupation не прошел проверку
        """
        not_valid_occupation = ['Рыцарь смерти', 'Воин', 'Друид', 'Шаман', 'Жрец', 'Паладин', 'Маг',
                                'Охотник на демонов', 'Чернокнижник', 'Разбойник', 'Монах']
        return re.match(r"[\w\ -]+", self.__occupation) is not None and self.__occupation not in not_valid_occupation

    def check_work_experience(self):
        """
        Проверка поля work_experience на валидность
        Если work_experience больше нуля или меньше 60 лет, то считается валидной
        :return: True - work_experience прошел проверку
                 False - work_experience не прошел проверку
        """
        return re.match(r"\-?\d+$", str(self.__work_experience)) is not None and int(
            self.__work_experience) >= 0 and int(self.__work_experience) <= 60

    def check_academic_degree(self):
        """
        Проверка поля academic_degree на валидность
        Если academic_degree - Бакалавр, Специалист, Магистр, Доктор наук, Аспирант, Кандидат наук, то запись валидная
        :return: True - academic_degree прошел проверку
                 False - academic_degree не прошел проверку
        """
        return self.__academic_degree == 'Бакалавр' or self.__academic_degree == 'Специалист' or \
               self.__academic_degree == 'Магистр' or self.__academic_degree == 'Доктор наук' or \
               self.__academic_degree == 'Аспирант' or self.__academic_degree == 'Кандидат наук'

    def check_worldview(self):
        """
        Проверка поля worldview на валидность
        Если worldview находится в списке valid_worldview ,то запись валидная
        :return: True - worldview прошел проверку
                 False - worldview не прошел проверку
        """
        valid_worldview = ['Секулярный гуманизм', 'Атеизм', 'Агностицизм', 'Иудаизм', 'Деизм', 'Пантеизм',
                           'Конфуцианство', 'Буддизм', 'Католицизм']
        return re.match(r"\w+",
                        str(self.__worldview)) is not None and self.__worldview in valid_worldview

    def check_address(self):
        """
        Проверка поля address на валидность
        Если address имеет вид "ул. **** nn" или "Аллея **** nn", то запись валидная
        :return: True - address прошел проверку
                 False - address не прошел проверку
        """
        return re.match(r"(ул\.\s[\w .-]+\d+)", self.__address) is not None or re.match(r"^Аллея\s[\w .-]+\d+$",
                                                                                        self.__address) is not None

    def check_all(self):
        """
        Проверка всех полей объекта класса Validator ан валидность
        :return: Словарь ошибок, где ключ - поле, значение (bool) - валидно ли поле по этому ключу или нет
        """
        err = dict({'email': True, 'height': True, 'inn': True, 'passport_number': True, 'occupation': True,
                    'work_experience': True, 'academic_degree': True, 'worldview': True, 'address': True})
        err['email'] = self.check_email()
        err['height'] = self.check_height()
        err['inn'] = self.check_inn()
        err['passport_number'] = self.check_passport_number()
        err['occupation'] = self.check_occupation()
        err['work_experience'] = self.check_work_experience()
        err['academic_degree'] = self.check_academic_degree()
        err['worldview'] = self.check_worldview()
        err['address'] = self.check_address()
        return err


parser = argparse.ArgumentParser(description='main.py')
input_filename = ""
output_filename = ""
parser.add_argument('-i', '--input', type=str, help='Путь к файлу, откуда считать данные', required=True,
                    dest='inputfilename')
parser.add_argument('-o', '--output', type=str, help='Путь к файлу, куда записать валидные данные', required=True,
                    dest='outputfilename')
args = parser.parse_args()
input_filename = os.path.realpath(args.inputfilename)
output_filename = os.path.realpath(args.outputfilename)
counter = 0
rfile = ReadFile(input_filename)
wfile = open(output_filename, 'w')
worldview = dict()
codes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
data_to_write = []
with tqdm(rfile.data, desc='Проверка записей') as progressbar:
    for elem in rfile.data:
        counter += 1
        check = Validator(elem['email'], elem['height'], elem['inn'], elem['passport_number'], elem['occupation'],
                          elem['work_experience'], elem['academic_degree'], elem['worldview'], elem['address'])
        err = check.check_all()
        code = 1
        if err['email'] and err['height'] and err['inn'] and err['passport_number'] and err['occupation'] and \
                err['work_experience'] and err['academic_degree'] and err['worldview'] and err['address']:
            codes[0] += 1
            code = 0
        if not err['email']:
            codes[1] += 1
        if not err['height']:
            codes[2] += 1
        if not err['height']:
            codes[3] += 1
        if not err['passport_number']:
            codes[4] += 1
        if not err['occupation']:
            codes[5] += 1
        if not err['work_experience']:
            codes[6] += 1
        if not err['academic_degree']:
            codes[7] += 1
        if not err['worldview']:
            codes[8] += 1
        if not err['address']:
            codes[9] += 1
        if code == 0:
            data_to_write.append(elem)
            """wfile.write("email: " + elem["email"] + "\n" + "height:" + str(elem["height"]) + "\n" +
                        "inn: " + str(elem["inn"]) + "\n" + "passport_number:" + str(elem["passport_number"]) + "\n" +
                        "occupation: " + elem["occupation"] + "\n" + "work_experience: " + str(elem["work_experience"])
                        + "\n" + "academic_degree: " + elem["academic_degree"] + "\n" + "worldview: " + elem[
                            "worldview"] +
                        "\n" + "address: " + elem["address"] + "\n" + "__________________________________________\n")
            """
        progressbar.update(1)
    json.dump(data_to_write, wfile)
wfile.close()
errors = codes[1] + codes[2] + codes[3] + codes[4] + codes[5] + codes[6] + codes[7] + codes[8] + codes[9]
print("Всего пользователей: " + str(counter) + "\nЧисло валидных записей - " + str(codes[0]) +
      "\nЧисло невалидных записей - " + str(errors))
print("Количество ошибок в поле email - ", codes[1], "\n", "Количество ошибок в поле height - ", codes[2], "\n",
      "Количество ошибок в поле inn - ", codes[3], "\n", "Количество ошибок в поле passport_number - ", codes[4], "\n",
      "Количество ошибок в поле occupation - ", codes[5], "\n", "Количество ошибок в поле work_experience - ", codes[6],
      "\n", "Количество ошибок в поле academic_degree - ", codes[7], "\n", "Количество ошибок в поле worldview - ",
      codes[8], "\n", "Количество ошибок в поле address - ", codes[9], "\n", sep='')
