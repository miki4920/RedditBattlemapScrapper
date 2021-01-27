import os
import re


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
        return name

    @staticmethod
    def get_url(submission):
        url = submission["url"]
        return url

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
        url = self.get_url(submission)
        extension = self.get_extension(url)
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
