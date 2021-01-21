from os import walk

tags = ['forest', 'cave', 'temple', 'river', 'ruins', 'night', 'mountain', 'dungeon', 'bridge', 'inn', 'tavern', 'desert', 'swamp', 'village', 'camp', 'crossing', 'castle', 'lair', 'fort', 'jungle', 'entrance', 'island', 'arena', 'pass', 'road', 'tomb', 'ruined', 'keep', 'city', 'tower', 'town']
minimum_tag_count = 5


class MapTagger(object):
    def __init__(self, path):
        self.word_dictionary = {}

        _, _, file_names = next(walk(path))
        for i in range(0, len(file_names)):
            self.iterate_through_word(file_names[i])
        self.word_dictionary = dict(sorted(self.word_dictionary.items(), key=lambda item: item[1])[::-1])
        self.word_dictionary = {k: v for k, v in self.word_dictionary.items() if v >= minimum_tag_count}
        print(list(self.word_dictionary.keys()))

    def iterate_through_word(self, file_name):
        for word in file_name.split("_")[:-1]:
            self.add_to_word_dictionary(word)
            if word in tags:
                pass

    def add_to_word_dictionary(self, word):
        if word in self.word_dictionary:
            self.word_dictionary[word] += 1
        else:
            self.word_dictionary[word] = 1




