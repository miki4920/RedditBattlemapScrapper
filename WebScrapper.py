import re
from UtilityFunctions import *
from HashFunctions import hash_image, hash_distance
from MapTagger import MapTagger
from DictionaryMaker import DictionaryMaker
from MapUploader import MapUploader
from SubmissionChecker import SubmissionChecker


base_url = "http://api.pushshift.io/reddit/search/submission/"
file_extensions = ["jpg", "png"]
starting_timestamp = 0

download_path = "Maps/"
temporary_path = "Temp/"
dictionary_path = "maps_dictionary.json"

image_similarity = 0

minimum_tag_repetitions = 5
base_tags = []
black_list_words = open("Config/black_list_words.txt", "r").read().split("\n")
stop_words = open("Config/stop_words.txt", "r").read().split("\n")
subreddits = read_json("Config/subreddits.json")
upload_ip = "http://127.0.0.1:8000/maps/"
minimum_file_size = 5000
maximum_file_size = 20485760

config = {"base_url": base_url,
          "file_extensions": file_extensions,
          "starting_timestamp": starting_timestamp,
          "download_path": download_path,
          "minimum_file_size": minimum_file_size,
          "maximum_file_size": maximum_file_size,
          "temporary_path": temporary_path,
          "dictionary_path": dictionary_path,
          "image_similarity": image_similarity,
          "base_tags": base_tags,
          "minimum_tag_repetitions": minimum_tag_repetitions,
          "stop_words": stop_words,
          "black_list_words": black_list_words,
          "subreddits": subreddits,
          "upload_ip": upload_ip}


class WebScrapper(object):
    def __init__(self, config):
        self.config = config
        self.dictionary_maker = DictionaryMaker(config)
        self.submission_checker = SubmissionChecker(config)
        self.submission_list = []
        if os.path.exists(self.config["dictionary_path"]):
            self.submission_list = read_json(self.config["dictionary_path"])

    def get_url(self, subreddit, timestamp):
        return self.config["base_url"] + f"?subreddit={subreddit}" \
                                         f"&score=>{subreddits[subreddit]['score']}" \
                                         f"&after={timestamp}&sort=asc&size=1000"

    def start_scrapping(self):
        timestamp = self.config["starting_timestamp"]

        for subreddit in config["subreddits"]:
            while True:
                url = self.get_url(subreddit, timestamp)
                json_data = request_file(url).json()["data"]
                if len(json_data) < 1:
                    break
                for submission in json_data:
                    if self.submission_checker.check_title(submission, subreddits[subreddit]["grid"]):
                        submission_dictionary = self.dictionary_maker.create_submission_dictionary(submission)
                        submission = request_file(submission_dictionary["url"]).content
                        submission_dictionary["hash"] = hash_image(submission)
                        if self.submission_checker.check_file_size(submission):
                            if self.submission_checker.check_hash(submission_dictionary["hash"], self.submission_list):
                                save_file(submission_dictionary["path"], submission)
                                self.submission_list.append(submission_dictionary)
                write_json(self.config['dictionary_path'], self.submission_list)
                timestamp = int(json_data[-1]["created_utc"])

#
# scrapper = WebScrapper(config)
# scrapper.start_scrapping()
map_tagger = MapTagger(config)
map_tagger.assign_tags()
map_uploader = MapUploader(config)
map_uploader.upload_dictionary()