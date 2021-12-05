import re
import json
import os
from package_validate_and_sort.sort import *
from package_validate_and_sort.validator_module import *
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser(description='main.py')
parser.add_argument('-i', '--input', type=str, help='Путь к файлу, откуда считать данные', required=True,
                    dest='inputfilename')
parser.add_argument('-o', '--output', type=str, help='Путь к файлу, куда записать валидные данные', required=True,
                    dest='outputfilename')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-v', '--validate', type=str, help="Аргумент, показывающий, что необходимо произвести валидацию",
                   dest='validate')
group.add_argument('-s', '--sort', type=str, help='Аргумент, показывающий, что необходимо произвести сортировку',
                   dest='sort')
args = parser.parse_args()

input_filename = os.path.realpath(args.inputfilename)
output_filename = os.path.realpath(args.outputfilename)
validate_flag = args.validate
sort_flag = args.sort
counter = 0
if validate_flag:
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
          "Количество ошибок в поле inn - ", codes[3], "\n", "Количество ошибок в поле passport_number - ", codes[4],
          "\n",
          "Количество ошибок в поле occupation - ", codes[5], "\n", "Количество ошибок в поле work_experience - ",
          codes[6],
          "\n", "Количество ошибок в поле academic_degree - ", codes[7], "\n", "Количество ошибок в поле worldview - ",
          codes[8], "\n", "Количество ошибок в поле address - ", codes[9], "\n", sep='')
elif sort_flag:
    data = data_from_json(input_filename)
    heapSort(data)
    pickle_serialization(data, "sorted_pickle.txt")
    new_data = pickle_deserialization("sorted_pickle.txt")