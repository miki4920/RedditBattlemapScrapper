import os
import re

from UtilityFunctions.FileFunctions import read_json, write_json
from ConfigFiles.Config import Config


def __filter_words(name):
    name_list = []
    for word in name.split("_"):
        if len(word) < 3:
            pass
        elif word in Config.stop_words:
            pass
        elif word in name_list:
            pass
        else:
            name_list.append(word)
    return "_".join(name_list)


def __simplify_name(name):
    name = name.lower()
    name = re.sub(r'[^a-zA-Z_]', '_', name)
    name = __filter_words(name)
    name = re.sub("(_)+", "_", name)
    name = re.sub("_$|^_", "", name)
    while len(name) > 40:
        name = "_".join(name.split("_")[:-1])
    if len(name) < 4:
        name = "review"
    return name


def __get_extension(url):
    return url[-3:]


def __get_path(name, extension):
    unique_name = name
    path = Config.download_path + unique_name + "." + extension
    count = 2
    while os.path.exists(path):
        unique_name = name + f"_{count}"
        path = Config.download_path + unique_name + "." + extension
        count += 1
    return unique_name, path


def __get_size(image_name):
    size = re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", image_name)
    return size.group(0) if size else False


def create_dictionary(submission):
    name = __simplify_name(submission["title"])
    url = submission["url"]
    extension = url[-3:]
    name, path = __get_path(name, extension)
    width, height = None, None
    if __get_size(submission["title"]):
        width, height = list(map(int, __get_size(submission["title"]).split("x")))
    dictionary = {"name": name,
                  "url": url,
                  "extension": extension,
                  "path": path,
                  "width": width,
                  "height": height,
                  "hash": None,
                  "tags": ()
                  }
    return dictionary


def update_stop_words():
    dictionary = read_json(Config.dictionary_path)
    for metadata in dictionary:
        name = __simplify_name(metadata["name"])
        temporary_path = Config.temporary_path + metadata["path"].replace(Config.download_path, "")
        os.rename(metadata["path"], temporary_path)
        name, path = __get_path(name, metadata["extension"])
        os.rename(temporary_path, path)
        metadata["name"] = name
        metadata["path"] = path
    write_json(Config.dictionary_path, dictionary)