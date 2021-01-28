from UtilityFunctions import *
from HashFunctions import hash_image, hash_distance
from MapTagger import MapTagger
from DictionaryMaker import DictionaryMaker
import os
import re

base_url = "http://api.pushshift.io/reddit/search/submission/"
subreddit = "battlemaps"
starting_timestamp = 0
minimum_submission_score = 10
gridded_only = True

download_path = "Maps/"
temporary_path = "Temp/"
dictionary_path = "maps_dictionary.json"

image_similarity = 0

minimum_tag_repetitions = 5
base_tags = []
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
              'floor', 'great', 'rpg', 'battlemaps', 'amp', 'encounter', 'tree', 'guard']

config = {"base_url": base_url,
          "subreddit": subreddit,
          "starting_timestamp": starting_timestamp,
          "minimum_submission_score": minimum_submission_score,
          "gridded_only": gridded_only,
          "download_path": download_path,
          "temporary_path": temporary_path,
          "dictionary_path": dictionary_path,
          "image_similarity": image_similarity,
          "base_tags": base_tags,
          "minimum_tag_repetitions": minimum_tag_repetitions,
          "stop_words": stop_words}


class WebScrapper(object):
    def __init__(self, dictionary_maker, config):
        self.dictionary_maker = dictionary_maker
        self.config = config
        self.submission_list = []

    @staticmethod
    def get_size(image_name):
        size = re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", image_name)
        return size.group(0) if size else False

    def check_submission(self, submission):
        if not re.search("i\..*\.it", submission["url"]):
            return False
        if self.config['gridded_only'] and not self.get_size(submission["title"]):
            return False
        return True

    def check_hash(self, image_hash):
        for submission in self.submission_list:
            if hash_distance(image_hash, submission["hash"]) <= self.config["image_similarity"]:
                return False
        return True

    def start_scrapping(self):
        timestamp = self.config["starting_timestamp"]
        if os.path.exists(self.config["dictionary_path"]):
            self.submission_list = read_json(self.config["dictionary_path"])
        while True:
            url = self.config["base_url"] + f"?subreddit={self.config['subreddit']}&score=>{self.config['minimum_submission_score']}&after={timestamp}&sort=asc&size=500"
            json_api = list(read_json(request_file(url)).values())[0]
            for submission in json_api:
                if self.check_submission(submission):
                    submission_dictionary = self.dictionary_maker.create_submission_dictionary(submission)
                    file = request_file(submission_dictionary["url"])
                    submission_dictionary["hash"] = hash_image(file)
                    if self.check_hash(submission_dictionary["hash"]) and check_file_size(file):
                        save_file(submission_dictionary["path"], file)
                        self.submission_list.append(submission_dictionary)
            write_json(self.config['dictionary_path'], self.submission_list)
            if len(json_api) < 1:
                break
            timestamp = int(json_api[-1]["created_utc"])


dictionary_maker = DictionaryMaker(config)
# scrapper = WebScrapper(dictionary_maker, config)
# scrapper.start_scrapping()
dictionary_maker.update_stop_words()
map_tagger = MapTagger(config)
map_tagger.assign_tags()