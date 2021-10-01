import zipfile
import os
import hashlib
import requests
import re

# os.mkdir("C:\\Users\\artio\\Documents\\Python_Labs\\arch")
directory_to_extract_to = 'C:\\Users\\artio\\Documents\\Python_Labs'
arch_file = 'C:\\Users\\artio\\Documents\\Python_Labs\\tiff-4.2.0_lab1.zip'
test_zip = zipfile.ZipFile(arch_file)
test_zip.extractall('C:\\Users\\artio\\Documents\\Python_Labs\\arch')
test_zip.close()

test_zip_files = test_zip.namelist()

txt_files = []
for r, d, f in os.walk(directory_to_extract_to):
    for file in f:
        if (file.find(".txt") != -1):
            target_file_data = open(r + "\\" + file, 'rb').read()
            result = hashlib.md5(target_file_data).hexdigest()
            print(r + "\\" + file, " hash =", result)
print("---" * 10)
url = ""
for r, d, f in os.walk(directory_to_extract_to):
    for file in f:
        target_file_data = open(r + "\\" + file, 'rb').read()
        result = hashlib.md5(target_file_data).hexdigest()
        if result == "4636f9ae9fef12ebd56cd39586d33cfb":
            print(r + '\\' + file, "\n", open(r + "\\" + file, 'r').read(), "\n\n")
            url = open(r + "\\" + file, 'r').read()

response = requests.get(url)
counter = 0
result_dct = {}
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', response.text)
cols_list = []
for line in lines:
    if counter == 0:
        headers = re.sub(r'<.*?>', ';', line)
        headers = re.sub(r'\(\+\d+(\s\d+)?\)', ';', headers)
        headers = re.sub(r'(^[А-Яа-я])\s', '', headers)
        headers = re.sub(r'[A-Za-z]+', '', headers)
        headers = re.sub(r'(;)+', '=', headers)
        headers = re.sub(r'=.(.)?\s\s', '', headers)
        headers = re.sub(r'\xa0', '', headers)
        headers = re.sub(r'\*', '', headers)
        headers = re.sub(r'_', '-1', headers)
        cols_list = list(filter(None, headers.split('=')))
        counter += 1
        continue
    else:
        headers = re.sub(r'<.*?>', ';', line)
        headers = re.sub(r'\(\+\d+(\s\d+)?\)', ';', headers)
        headers = re.sub(r'(^[А-Яа-я])\s', '', headers)
        headers = re.sub(r'[A-Za-z]+', '', headers)
        headers = re.sub(r'(;)+', '=', headers)
        headers = re.sub(r'=.(.)?\s\s', '', headers)
        headers = re.sub(r'\xa0', '', headers)
        headers = re.sub(r'\*', '', headers)
        headers = re.sub(r'_', '-1', headers)

    country_list = list(filter(None, headers.split('=')))
    country_name = country_list[0]
    col1_val = country_list[1]
    col2_val = country_list[2]
    col3_val = country_list[3]
    col4_val = country_list[4]

    result_dct[country_name] = {}
    result_dct[country_name][cols_list[0]] = int(col1_val)
    result_dct[country_name][cols_list[1]] = int(col2_val)
    result_dct[country_name][cols_list[2]] = int(col3_val)
    result_dct[country_name][cols_list[3]] = int(col4_val)
    print(country_name, result_dct[country_name])
    counter += 1
print("\n")

#  Task 5

output = open('C:\\Users\\artio\\Documents\\Python_Labs\\data.csv', 'w')
cols_string = ';'.join(cols_list)
counter = 0

for key in result_dct.keys():
    if counter == 0:
        cols_string = "Страна;" + cols_string
        output.write(cols_string)
        output.write("\n")
        counter += 1
    output.write(key + ';')
    col_values_string = ""
    for col in cols_list:
        col_values_string = col_values_string + str(result_dct[key][col]) + ';'
    output.write(col_values_string)
    output.write('\n')
output.close()

target_country = input("Введите название страны: ")
print(target_country, result_dct[target_country])
