from os import walk
import re

map_format = [".jpg", ".png"]
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
              'oc', 'free', 'ocart', 'comments','gridless', 'grid', 'made', 'battlemapoc', 'inspired', 'level',
              'storey', 'three', 'maps']


class MapTagger(object):
    def __init__(self, path):
        self.word_dictionary = {}
        _, _, self.file_names = next(walk(path))
        self.create_word_dictionary()

    def create_word_dictionary(self):
        for file_name in self.file_names:
            file_name = re.sub("(\d+x(\d+)+)", "", file_name)
            for extension in map_format:
                file_name = file_name.replace(extension, "")
            file_name = re.sub(r'\W+', '', file_name)
            file_name = file_name.lower()
            file_name = re.sub(r'\d+', '', file_name)
            file_name = re.sub("(_)+", "_", file_name)
            print(file_name)
            file_name = file_name.split("_")
            for word in file_name:
                if len(word) < 2:
                    pass
                elif word in stop_words:
                    pass
                else:
                    if word in self.word_dictionary:
                        self.word_dictionary[word] += 1
                    else:
                        self.word_dictionary[word] = 1
        word_dictionary = {k: v for k, v in sorted(self.word_dictionary.items(), key=lambda item: item[1])[::-1]}
        self.word_dictionary = {k: v for k, v in word_dictionary.items() if v > 8}
        print(self.word_dictionary)



map_tagger = MapTagger(root)