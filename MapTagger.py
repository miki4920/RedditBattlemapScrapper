from os import walk
import re
from UtilityFunctions import find_file_extension, change_file_name

map_format = [".jpg", ".png"]
root = "Maps/"
create_dictionary = True
minimum_tag_count = 9
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
              'storey', 'three', 'maps', 'feedback', 'handdrawn', 'part', 'px']

tags = ['forest', 'temple', 'ruins', 'dungeon', 'lair', 'mountain', 'desert', 'night', 'river', 'village', 'path',
        'bridge', 'camp', 'tavern', 'town', 'city', 'castle', 'island', 'swamp', 'cave', 'ancient', 'entrance',
        'crossing', 'tower', 'fort', 'snowy', 'frozen', 'lake', 'inn', 'winter', 'crossroads', 'throne', 'pass',
        'library', 'small', 'dwarven']


class MapTagger(object):
    def __init__(self, path):
        self.word_dictionary = {}
        self.map_dictionary = {}

        _, _, file_names = next(walk(path))
        for i in range(0, len(file_names)):
            file_name = self.simplify_map_title(file_names[i])


        self.word_dictionary = dict(sorted(self.word_dictionary.items(), key=lambda item: item[1])[::-1])
        self.word_dictionary = {k: v for k, v in self.word_dictionary.items() if v >= minimum_tag_count}
        if create_dictionary:
            print(self.word_dictionary.values())

    @staticmethod
    def simplify_map_title(file_name):
        file_name = file_name.lower()
        file_size = re.search("(\d+x(\d+)+)", file_name).group(0)
        file_extension = find_file_extension(file_name)

        file_name = file_name.replace(file_size, "")
        file_name = file_name.replace(file_extension, "")

        file_name = re.sub(r'\W+', '', file_name)
        file_name = re.sub(r'\d+', '', file_name)
        file_name = re.sub("(_)+", "_", file_name)

        return file_name, file_size, file_extension

    def iterate_through_word(self, file_name):
        map_tags = []
        for word in file_name.split("_"):
            if len(word) < 2:
                pass
            elif word in stop_words:
                pass
            elif create_dictionary:
                self.add_to_word_dictionary(word)
            elif word in tags:
                map_tags.append(word)




    def add_to_word_dictionary(self, word):
        if word in self.word_dictionary:
            self.word_dictionary[word] += 1
        else:
            self.word_dictionary[word] = 1




map_tagger = MapTagger(root)
