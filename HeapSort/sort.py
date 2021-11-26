import pickle
import json


def data_from_json(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as rfile:
        data = json.load(rfile)
    return data


def heapify(arr, n, i):
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


def heapSort(arr: list):
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


def pickle_serialization(data: list, path: str) -> None:
    with open(path, 'wb') as wfile:
        pickle.dump(data, wfile)


def pickle_deserialization(path: str) -> list:
    with open(path, 'rb') as rfile:
        data = pickle.load(rfile)
    return data


data = data_from_json(r"C:\Users\artio\PycharmProjects\First_Python_Lab\63res.txt")
heapSort(data)
pickle_serialization(data, "sorted.txt")
new_data = pickle_deserialization("sorted.txt")
print(new_data)
