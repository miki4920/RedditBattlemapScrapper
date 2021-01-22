import requests
import os
import json
import re


extensions = [".jpg", ".png"]
minimum_image_size = 50000
maximum_image_size = 20485760
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
              'three', 'roll', 'virtual', 'version', 'multi', 'original', 'mine', 'four', 'five', 'ppi', 'square',
              'small', 'multi', 'jpg', 'png', 'inktober', 'scale', 'first', 'units', 'grand', 'assets', 'mapvember',
              'floor', 'great', 'rpg']


def request_file(url):
    return requests.get(url).content


def read_file(path):
    with open(root+path, 'rb') as file:
        return file.read()


def save_file(path, content):
    path = root + path
    if check_file_size(content) and not os.path.exists(path):
        with open(path, "wb") as file:
            file.write(content)


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
    return minimum_image_size < len(file) < maximum_image_size


def simplify_name(name):
    name = name.lower()
    extension = find_file_extension(name)
    name = re.sub(r'\W+', '_', name)

    size = re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", name)

    name = re.sub(r'[^a-zA-Z_]', '_', name)
    name = filter_words(name)
    name = re.sub("(_)+", "_", name)
    name = re.sub("_$|^_", "", name)

    if size:
        name = name.replace(size.group(0), "_")
        name += "_" + f"{size.group(0)}"

    name = filter_words(name) + extension
    return name


def simplify_all_names(root_path):
    _, _, file_names = next(os.walk(root_path))
    for i in range(0, len(file_names)):
        file_path = file_names[i]
        file_content = read_file(file_path)
        os.remove(root_path + file_path)
        file_name = simplify_name(file_path)
        save_file(file_name, file_content)


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



