from os import walk
from UtilityFunctions import read_file


class MapTagger(object):
    def __init__(self, path, minimum_maps_per_tag):
        self.word_dictionary = self.add_to_word_dictionary(path)
        self.word_dictionary = dict(sorted(self.word_dictionary.items(), key=lambda item: item[1])[::-1])
        self.word_dictionary = {k: v for k, v in self.word_dictionary.items() if v >= minimum_maps_per_tag}

    @staticmethod
    def add_to_word_dictionary(path):
        _, _, file_names = next(walk(path))
        tag_dictionary = {}
        for i in range(0, len(file_names)):
            for word in file_names[i].split("_")[:-1]:
                if word in tag_dictionary:
                    tag_dictionary[word] += 1
                else:
                    tag_dictionary[word] = 1
        return tag_dictionary

    def get_tags(self, file_name):
        tags = []
        for word in file_name:
            if word in self.word_dictionary and word not in tags:
                tags.append(word)
        tags = [('tags', tag) for tag in tags]
        return tags

    def get_metadata_dictionary(self, path):
        _, _, file_names = next(walk(path))
        map_dictionary = {}
        for i in range(0, len(file_names)):
            file_name = file_names[i].split("_")

            tags = self.get_tags(file_name[:-1])
            size = file_name[-1][:-4].split("x")
            extension = file_name[-1][-3:]

            file_name = file_name[:-1]
            file_name = "_".join(file_name) + "." + extension
            map_dictionary[file_names[i]] = [("image", (file_name, read_file(file_names[i]), f"image/{extension}")),
                                             ('name', 'nick'), ('squareWidth', size[0]),
                                             ('squareHeight', size[1]), ('tags', 'battlemap')] + tags
        return map_dictionary
