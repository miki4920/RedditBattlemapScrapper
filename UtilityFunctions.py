import requests
import os
import json


def request_file(url):
    return requests.get(url).content


def check_if_file_exists(path):
    return os.path.exists(path)


def save_file(path, content):
    with open(path, "wb") as file:
        file.write(content)


def read_json(file):
    return json.loads(request_file(file))
