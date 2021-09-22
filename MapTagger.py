from UtilityFunctions.FileFunctions import *
from Config import CONFIG


class MapTagger(object):
    def __init__(self):
        self.dictionary = read_json(CONFIG.dictionary_path)
        self.tags = []

    def get_name_tags(self):
        name_tags = {}
        for submission in self.dictionary:
            for tag in submission["name"].split("_"):
                if len(tag) < 3:
                    pass
                elif tag in self.tags:
                    pass
                else:
                    if tag in name_tags:
                        name_tags[tag] += 1
                    else:
                        name_tags[tag] = 1
        name_tags = dict(sorted(name_tags.items(), key=lambda item: item[1])[::-1])
        name_tags = {k: v for k, v in name_tags.items() if v >= CONFIG.minimum_tag_repetitions}
        self.tags.extend(list(name_tags.keys()))

    def assign_tags(self):
        self.get_name_tags()
        for submission in self.dictionary:
            submission_tags = []
            for tag in submission["name"].split("_"):
                if tag in self.tags and tag not in submission_tags:
                    submission_tags.append(tag)
            submission["tags"] = submission_tags
        write_json(CONFIG.dictionary_path, self.dictionary)



