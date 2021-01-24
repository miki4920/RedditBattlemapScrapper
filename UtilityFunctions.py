import requests
import os
import json
import time


minimum_image_size = 50000
maximum_image_size = 20485760
root = "Maps/"


def request_file(url):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    print(url)
    url = url.replace("preview", "i", 1)
    url = url.replace("external-", "")
    time.sleep(2)
    return requests.get(url, headers=headers).content


def read_file(path):
    with open(root+path, 'rb') as file:
        return file.read()


def save_file(path, content):
    if check_file_size(content):
        with open(path, "wb") as file:
            file.write(content)


def read_json(file):
    request = request_file(file)
    try:
        return json.loads(request)
    except ValueError:
        print("error")


def change_file_name(path, new_name):
    os.rename(path, new_name)


def check_file_size(file):
    return minimum_image_size < len(file) < maximum_image_size






