import re
import json
import os


class ReadFile:
    __data: object

    def __init__(self, path: str):
        try:
            if os.path.exists(path):
                self.__data = json.load(open(path, encoding='windows-1251'))
        except OSError:
            print("Файл по данному пути не существует")

    @property
    def data(self):
        return self.__data


class Validator:
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
        self.__email = email
        self.__height = height
        self.__inn = inn
        self.__passport_number = passport_number
        self.__occupation = occupation
        self.__work_experience = work_experience
        self.__academic_degree = academic_degree
        self.__worldview = worldview
        self.__address = address

    @property
    def email(self):
        return self.__email

    def check_email(self):
        return re.match(r"[\w\.\d-]+@\w+\.\w+", self.__email) is not None

    def check_height(self):
        return re.match(r"\-?\d+\.\d+",
                        str(self.__height)) is not None and float(self.__height) >= 0.67 and float(
            self.__height) <= 2.30

    def check_inn(self):
        return re.match(r"\d{12}", str(self.__inn)) is not None

    def check_passport_number(self):
        return re.match(r"\d{6}", str(self.__passport_number)) is not None

    def check_occupation(self):
        return re.match(r"[\w\ -]+", self.__occupation) is not None

    def check_work_experience(self):
        return re.match(r"\-?\d+$", str(self.__work_experience)) is not None \
               and int(self.__work_experience) >= 0 and int(self.__work_experience) <= 60

    def check_academic_degree(self):
        return self.__academic_degree == 'Бакалавр' or self.__academic_degree == 'Специалист' or \
               self.__academic_degree == 'Магистр' or self.__academic_degree == 'Доктор наук' or \
               self.__academic_degree == 'Аспирант' or self.__academic_degree == 'Кандидат наук'

    def check_worldview(self):
        return re.match(r"\w+", str(self.__work_experience)) is not None

    def check_address(self):
        return re.match(r"(ул\.\s[\w .-]+\d+)", self.__address) is not None or re.match(r"^Аллея\s[\w .-]+\d+$",
                                                                                        self.__address) is not None

    def check_all(self):
        if not self.check_email():
            return 1
        elif not self.check_height():
            return 2
        elif not self.check_inn():
            return 3
        elif not self.check_passport_number():
            return 4
        elif not self.check_occupation():
            return 5
        elif not self.check_work_experience():
            return 6
        elif not self.check_academic_degree():
            return 7
        elif not self.check_worldview():
            return 8
        elif not self.check_address():
            return 9
        else:
            return 0


counter = 0
codes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
rfile = ReadFile("63.txt")
wfile = open("result63.txt", 'w')
for elem in rfile.data:
    counter += 1
    check = Validator(elem['email'], elem['height'], elem['inn'], elem['passport_number'], elem['occupation'],
                      elem['work_experience'], elem['academic_degree'], elem['worldview'], elem['address'])
    code = check.check_all()
    codes[code] += 1

    if code == 0:
        wfile.write("email: " + elem["email"] + "\n" + "height:" + str(elem["height"]) + "\n" +
                    "inn: " + str(elem["inn"]) + "\n" + "passport_number:" + str(elem["passport_number"]) + "\n" +
                    "occupation: " + elem["occupation"] + "\n" + "work_experience: " + str(elem["work_experience"]) +
                    "\n" + "academic_degree: " + elem["academic_degree"] + "\n" + "worldview: " + elem["worldview"] +
                    "\n" + "address: " + elem["address"] + "\n" + "__________________________________________\n")
wfile.close()
errors = codes[1] + codes[2] + codes[3] + codes[4] + codes[5] + codes[6] + codes[7] + codes[8] + codes[9]
print("Количество ошибок из-за опредленных полей: \nВсего пользователей: " + str(
    counter) + "\nЧисло валидных записей - " + str(codes[0]) + "\nЧисло невалидных записей - " + str(errors))
