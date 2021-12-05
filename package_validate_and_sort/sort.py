import pickle
import json


def data_from_json(path: str) -> list:
    """
    Считывает файл с валидными записями по пути file
    :param path: str: Путь до файла
    :return: list: Список считанных записей
    """
    with open(path, 'r', encoding='utf-8') as rfile:
        data = json.load(rfile)
    return data


def heapify(arr, n, i):
    """
    Приводит дерево к виду, когда левый и правый элемент дерева больше, чем корень
    :param arr: List считанных данных для сортировки
    :param n: Количество элементов в arr
    :param i: Индекс узла дерева
    :return:
    """
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and float(arr[i]['height']) < float(arr[l]['height']):
        largest = l
    if r < n and float(arr[largest]['height']) < float(arr[r]['height']):
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heapSort(arr: list) -> None:
    """
    Пирамидальная сортировка
    :param arr: List, который необходимо отсортировать
    :return: None
    """
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


def pickle_serialization(data: list, path: str) -> None:
    """
    Сериализация отсортированного List'а данных в файл с помощью picle
    :param data: List, который необходимо сериализовать
    :param path: Путь, по которому необходимо сериализовать данные в файл
    :return: None
    """
    with open(path, 'wb') as wfile:
        pickle.dump(data, wfile)


def pickle_deserialization(path: str) -> list:
    """
    Десериализация данных, сериализованных в файл с помощью picle
    :param path: Путь, по которому необходимо десериализовать файл
    :return: None
    """
    with open(path, 'rb') as rfile:
        data = pickle.load(rfile)
    return data
