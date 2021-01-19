import requests
import os
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


extensions = [".jpg", ".png"]


def request_file(url):
    return requests.get(url).content


def upload_file(url, data):
    response = requests.post(url, data=data, headers={'Content-Type': data.content_type})
    return response


def check_if_file_exists(path):
    return os.path.exists(path)


def save_file(path, content):
    with open(path, "wb") as file:
        file.write(content)


def read_json(file):
    return json.loads(request_file(file))


def find_file_extension(path):
    for extension in extensions:
        if extension in path:
            return extension
    return False


def change_file_name(path, new_name):
    os.rename(path, new_name)



