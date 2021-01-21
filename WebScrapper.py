import os
import praw
from ClientSecrets import token
from UtilityFunctions import *
from MapTagger import MapTagger
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

token()
url_base = "http://api.pushshift.io/reddit/search/submission/"
subreddit = "battlemaps"
score = 10
starting_timestamp = 0
root = "Maps/"
minimum_maps_per_tag = 5


class WebScrapper(object):
    def __init__(self):
        self.reddit = praw.Reddit(client_id=os.environ["CLIENT_ID"],
                                  client_secret=os.environ["SECRET_KEY"],
                                  user_agent="WebScrapper",
                                  username="PythonScrapper",
                                  password=os.environ["REDDIT_PASSWORD"] )
        self.reddit.read_only = True
        self.start_scrapping(starting_timestamp)

    def start_scrapping(self, timestamp):
        while True:
            url = url_base + f"?subreddit={subreddit}&score=>{score}&after={timestamp}&sort=asc&size=500"
            json_api = read_json(url)["data"]
            for submission in json_api:
                submission = self.reddit.submission(url=submission["full_link"])
                self.save_submission(submission)
            timestamp = int(json_api[-1]["created_utc"])
            if len(json_api) < 1:
                return

    @staticmethod
    def save_submission(submission):
        file_extension = find_file_extension(submission.url)
        if file_extension and re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", submission.title):
            image_name = simplify_name(submission.title + file_extension)
            print(image_name)
            image = request_file(submission.url)
            save_file(image_name, image)


# scrapper = WebScrapper()
simplify_all_names(root)
map_tagger = MapTagger(root, minimum_maps_per_tag)
metadata_dictionary = map_tagger.get_metadata_dictionary(root)

for map in list(metadata_dictionary.values()):
    multipart_data = MultipartEncoder(
        fields=map
    )
    print(map[0][1][0])
    response = requests.post('http://192.168.0.40/imageUpload', data=multipart_data,
                      headers={'Content-Type': multipart_data.content_type})

    print(str(response) + " " + str(response.content))