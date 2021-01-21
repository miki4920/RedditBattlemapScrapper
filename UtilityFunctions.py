import requests
import os
import json


extensions = [".jpg", ".png"]
minimum_image_size = 50000
root = "Maps/"
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
              'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
              'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these',
              'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
              'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
              'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
              'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
              'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
              'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
              'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'map', 'battlemap', 'battle',
              'oc', 'free', 'ocart', 'comments', 'gridless', 'grid', 'made', 'battlemapoc', 'inspired', 'level',
              'storey', 'three', 'maps', 'feedback', 'handdrawn', 'part', 'px', 'xpx', 'art', 'info', 'one', 'two',
              'three', 'roll', 'virtual', 'version', 'multi', 'original', 'mine', 'four', 'five', 'ppi', 'square', 'small']


def request_file(url):
    return requests.get(url).content


def read_json(file):
    return json.loads(request_file(file))


def find_file_extension(path):
    for extension in extensions:
        if path.endswith(extension):
            return extension
    return False


def change_file_name(path, new_name):
    os.rename(path, new_name)


def check_file_size(file):
    return len(file) > minimum_image_size


def save_file(path, content):
    path = root + path
    if not os.path.exists(path) and check_file_size(content):
        with open(path, "wb") as file:
            file.write(content)


def filter_words(name):
    image_name_list = []
    for word in name.split("_"):
        if len(word) < 3:
            pass
        elif word in stop_words:
            pass
        elif word in image_name_list:
            pass
        else:
            image_name_list.append(word)
    return "_".join(image_name_list)


