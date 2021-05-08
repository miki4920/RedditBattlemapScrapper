from ConfigFiles.Config import Config
from UtilityFunctions.DictionaryFunctions import create_dictionary
from UtilityFunctions.HashFunctions import hash_image
from MapTagger import MapTagger
from MapUploader import MapUploader
from UtilityFunctions.NetworkFunctions import get_api_url, request_file
from UtilityFunctions.SubmissionFunctions import check_title, check_file_size, check_hash
from UtilityFunctions.FileFunctions import *


class WebScrapper(object):
    def __init__(self):
        self.submission_list = read_json(Config.dictionary_path)

    def get_submission(self, submission, subreddit):
        if check_title(submission, Config.subreddits[subreddit]["grid"]):
            submission_dictionary = create_dictionary(submission)
            submission = request_file(submission_dictionary["url"], timeout=1).content
            submission_dictionary["hash"] = hash_image(submission)
            if check_file_size(submission) and check_hash(submission_dictionary["hash"], self.submission_list):
                write_file(submission_dictionary["path"], submission)
                self.submission_list.append(submission_dictionary)

    def scrapper(self):
        for subreddit in Config.subreddits:
            timestamp = Config.starting_timestamp
            while True:
                url = get_api_url(subreddit, timestamp)
                try:
                    json_data = request_file(url).json()["data"]
                    if len(json_data) < 1:
                        break
                    for submission in json_data:
                        self.get_submission(submission, subreddit)
                    timestamp = int(json_data[-1]["created_utc"])
                except json.decoder.JSONDecodeError:
                    timestamp += 100
            write_json(Config.dictionary_path, self.submission_list)


map_uploader = MapUploader()
map_uploader.upload_dictionary()