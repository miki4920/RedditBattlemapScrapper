import requests
import os
import json
import time


def request_file(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    request = requests.get(url, headers=headers)
    time.sleep(1)
    return request


def save_file(path, content):
    with open(path, "wb") as file:
        file.write(content)


def read_json(json_object):
    if os.path.exists(json_object):
        with open(json_object, 'rb') as file:
            json_object = file.read()
    return json.loads(json_object)


def write_json(path, content):
    with open(path, 'w') as file:
        json.dump(content, file, indent=4)




