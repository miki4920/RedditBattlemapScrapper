import os
import re

from UtilityFunctions import read_json, write_json


class DictionaryMaker(object):
    def __init__(self, config):
        self.config = config

    def filter_words(self, name):
        name_list = []
        for word in name.split("_"):
            if len(word) < 3:
                pass
            elif word in self.config["stop_words"]:
                pass
            elif word in name_list:
                pass
            else:
                name_list.append(word)
        return "_".join(name_list)

    def simplify_name(self, name):
        name = name.lower()

        name = re.sub(r'[^a-zA-Z_]', '_', name)
        name = self.filter_words(name)
        name = re.sub("(_)+", "_", name)
        name = re.sub("_$|^_", "", name)
        while len(name) > 40:
            name = "_".join(name.split("_")[:-1])
        if len(name) < 4:
            name = "review"
        return name

    def update_stop_words(self):
        dictionary = read_json(self.config["dictionary_path"])
        for metadata in dictionary:
            name = self.simplify_name(metadata["name"])
            temporary_path = self.config["temporary_path"] + metadata["path"].replace(self.config["download_path"], "")
            os.rename(metadata["path"], temporary_path)
            name, path = self.get_path(name, metadata["extension"])
            os.rename(temporary_path, path)
            metadata["name"] = name
            metadata["path"] = path
        write_json(self.config["dictionary_path"], dictionary)

    @staticmethod
    def get_extension(url):
        return url[-3:]

    def get_path(self, name, extension):
        unique_name = name
        path = self.config["download_path"] + unique_name + "." + extension
        count = 2
        while os.path.exists(path):
            unique_name = name + f"_{count}"
            path = self.config["download_path"] + unique_name + "." + extension
            count += 1
        return unique_name, path

    @staticmethod
    def get_size(image_name):
        size = re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", image_name)
        return size.group(0) if size else False

    def create_submission_dictionary(self, submission):
        name = self.simplify_name(submission["title"])
        url = submission["url"]
        extension = url[-3:]
        name, path = self.get_path(name, extension)
        width, height = None, None
        if self.get_size(submission["title"]):
            width, height = list(map(int, self.get_size(submission["title"]).split("x")))
        submission_dictionary = {"name": name,
                                 "url": url,
                                 "extension": extension,
                                 "path": path,
                                 "width": width,
                                 "height": height,
                                 "hash": None,
                                 "tags": ()
                                 }
        return submission_dictionary
