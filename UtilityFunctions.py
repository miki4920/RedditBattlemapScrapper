import requests
import os
import json
import time


minimum_image_size = 5000
maximum_image_size = 20485760


def request_file(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    request = requests.get(url, headers=headers).content
    time.sleep(1)
    return request


def read_file(path):
    with open(path, 'rb') as file:
        return file.read()


def save_file(path, content):
    with open(path, "wb") as file:
        file.write(content)


def read_json(json_object):
    if os.path.exists(json_object):
        json_object = read_file(json_object)
    return json.loads(json_object)


def write_json(path, content):
    with open(path, 'w') as file:
        json.dump(content, file, indent=4)


def change_file_name(path, new_name):
    os.rename(path, new_name)


def check_file_size(file):
    return minimum_image_size < len(file) < maximum_image_size






