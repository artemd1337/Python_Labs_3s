import re
import json
import os


class ReadFile:
    """
       Класс File для чтения из текстового файла

       __data : object
       Содержит считанные данные из текстового файла
    """
    __data: list

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
