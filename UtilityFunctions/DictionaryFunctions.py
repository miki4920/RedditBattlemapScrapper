import os
import re

from UtilityFunctions.FileFunctions import read_json
from Config import CONFIG


class DictionaryMaker:
    def __init__(self):
        self.stop_words = set(read_json(CONFIG.stop_words_path))

    def __call__(self, submission, timestamp):
        name = self.simplify_name(submission["title"])
        square_width, square_height = self.get_square_size(submission["title"])
        url = submission["url"]
        extension = url[-3:]
        name, path = self.get_path(name, extension)
        dictionary = {"name": name,
                      "url": url,
                      "extension": extension,
                      "path": path,
                      "width": None,
                      "height": None,
                      "square_width": square_width,
                      "square_height": square_height,
                      "hash": None,
                      "tags": (),
                      "timestamp": timestamp,
                      }
        return dictionary

    def filter_function(self, word):
        if len(word) < 3:
            return False
        elif word in self.stop_words:
            return False
        return True

    def filter_words(self, name):
        name = name.split("_")
        word_list = filter(self.filter_function, name)
        return "_".join(word_list)

    def simplify_name(self, name):
        name = name.lower()
        name = re.sub(r"[^a-zA-Z_]", "_", name)
        name = re.sub(r"_+", "_", name)
        name = self.filter_words(name)
        name = re.sub(r"_+", "_", name)
        name = re.sub("_$|^_", "", name)
        while len(name) > CONFIG.name_length:
            name = "_".join(name.split("_")[:-1])
        if len(name) < 4:
            name = "review"
        return name

    @staticmethod
    def get_extension(url):
        return url[-3:]

    @staticmethod
    def get_path(name, extension):
        unique_name = name
        path = CONFIG.download_path + unique_name + "." + extension
        count = 2
        while os.path.exists(path):
            unique_name = name + f"_{count}"
            path = CONFIG.download_path + unique_name + "." + extension
            count += 1
        return unique_name, path

    @staticmethod
    def get_square_size(image_name):
        size = re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", image_name)
        if not size:
            return None, None
        size = size.group(0)
        size = size.split("x")
        size = [int(number) for number in size]
        return size
