import re

from io import BytesIO
from PIL import Image

from Config import CONFIG
from MapTagger import MapTagger
from MapUploader import MapUploader
from UtilityFunctions.DictionaryFunctions import DictionaryMaker
from UtilityFunctions.HashFunctions import hash_image
from UtilityFunctions.NetworkFunctions import get_api_url, request_file
from UtilityFunctions.FileFunctions import *


class WebScrapper(object):
    def __init__(self):
        self.submission_list = read_json(CONFIG.dictionary_path)
        self.subreddits = read_json(CONFIG.subreddits_path)
        self.black_list_words = set(read_json(CONFIG.black_list_words_path))
        self.dictionary_maker = DictionaryMaker()
        self.hash_set = set([submission["hash"] for submission in self.submission_list])

    @staticmethod
    def image_format(submission):
        return submission["url"][-3:] not in CONFIG.file_extensions

    @staticmethod
    def image_origin(submission):
        return not re.search("i\..*\.it", submission["url"])

    def blacklist(self, submission):
        image_name = submission["title"].lower()
        return any([word in image_name for word in self.black_list_words])

    def check_title(self, submission):
        if self.image_format(submission):
            return False
        if self.image_origin(submission):
            return False
        if self.blacklist(submission):
            return False
        if DictionaryMaker.get_square_size(submission["title"])[0] is None and CONFIG.square_size:
            return False
        return True

    @staticmethod
    def check_file_size(submission):
        return CONFIG.minimum_file_size < len(submission) < CONFIG.maximum_file_size

    def get_submission(self, submission):
        if self.check_title(submission):
            submission_dictionary = self.dictionary_maker(submission, submission["created_utc"])
            submission = request_file(submission_dictionary["url"], timeout=1).content
            submission_dictionary["width"], submission_dictionary["height"] = Image.open(BytesIO(submission)).size
            submission_dictionary["hash"] = hash_image(submission)
            if self.check_file_size(submission) and submission_dictionary["hash"] not in self.hash_set:
                write_file(submission_dictionary["path"], submission)
                self.submission_list.append(submission_dictionary)
                self.hash_set.add(submission_dictionary["hash"])

    def scrapper(self):
        for subreddit in self.subreddits:
            timestamp = 0
            while True:
                url = get_api_url(subreddit, timestamp)
                try:
                    json_data = request_file(url).json()["data"]
                    if len(json_data) < 1:
                        break
                    for submission in json_data:
                        self.get_submission(submission)
                    timestamp = int(json_data[-1]["created_utc"])
                except json.decoder.JSONDecodeError:
                    timestamp += 1000
                write_json(CONFIG.dictionary_path, self.submission_list)


if __name__ == "__main__":
    webscrapper = WebScrapper()
    webscrapper.scrapper()
    # map_tagger = MapTagger()
    # map_tagger.assign_tags()
    # map_uploader = MapUploader()
    # map_uploader.upload_dictionary()