import os
import praw
from Image import Image
from ClientSecrets import token
from UtilityFunctions import read_json
from MapTagger import MapTagger

token()
url_base = "http://api.pushshift.io/reddit/search/submission/"
subreddit = "battlemaps"
score = 10
starting_timestamp = 0


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
                image = Image(submission)
                image.save()
            timestamp = int(json_api[-1]["created_utc"])
            if len(json_api) < 1:
                return


# scrapper = WebScrapper()
tokeniser = MapTagger("Maps/")