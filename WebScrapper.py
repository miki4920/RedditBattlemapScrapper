import re
from UtilityFunctions import *
from HashFunctions import hash_image, hash_distance
from MapTagger import MapTagger
from DictionaryMaker import DictionaryMaker
from MapUploader import MapUploader


base_url = "http://api.pushshift.io/reddit/search/submission/"
subreddit = "battlemaps"
file_extensions = ["jpg", "png"]
starting_timestamp = 0
minimum_submission_score = 10
gridded_only = True

download_path = "Maps/"
temporary_path = "Temp/"
dictionary_path = "maps_dictionary.json"

image_similarity = 0

minimum_tag_repetitions = 5
base_tags = []
black_list_words = open("black_list_words.txt", "r").read().split("\n")
stop_words = open("stop_words.txt", "r").read().split("\n")
upload_ip = "http://127.0.0.1:8000/maps/"

config = {"base_url": base_url,
          "subreddit": subreddit,
          "file_extensions": file_extensions,
          "starting_timestamp": starting_timestamp,
          "minimum_submission_score": minimum_submission_score,
          "gridded_only": gridded_only,
          "download_path": download_path,
          "temporary_path": temporary_path,
          "dictionary_path": dictionary_path,
          "image_similarity": image_similarity,
          "base_tags": base_tags,
          "minimum_tag_repetitions": minimum_tag_repetitions,
          "stop_words": stop_words,
          "black_list_words": black_list_words,
          "upload_ip": upload_ip}


class WebScrapper(object):
    def __init__(self, dictionary_maker, config):
        self.dictionary_maker = dictionary_maker
        self.config = config
        self.submission_list = []

    def is_in_blacklist(self, image_name):
        image_name = image_name.lower()
        for word in self.config["black_list_words"]:
            if word in image_name:
                return False
        return True

    @staticmethod
    def get_size(image_name):
        size = re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", image_name)
        return size.group(0) if size else False

    def check_submission(self, submission):
        if submission["url"][-3:] not in self.config["file_extensions"]:
            return False
        if not re.search("i\..*\.it", submission["url"]):
            return False
        if not self.is_in_blacklist(submission["title"]):
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
            url = self.config[
                      "base_url"] + f"?subreddit={self.config['subreddit']}&score=>{self.config['minimum_submission_score']}&after={timestamp}&sort=asc&size=100"
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
scrapper = WebScrapper(dictionary_maker, config)
scrapper.start_scrapping()
dictionary_maker.update_stop_words()
map_tagger = MapTagger(config)
map_tagger.assign_tags()
map_uploader = MapUploader(config)
map_uploader.upload_dictionary()