import os
import praw
from Image import Image
from ClientSecrets import token
from UtilityFunctions import read_json

token()
url_base = "http://api.pushshift.io/reddit/search/submission/"
subreddit = "FantasyMaps"
score = 100


class WebScrapper(object):
    def __init__(self):
        self.reddit = praw.Reddit(client_id=os.environ["CLIENT_ID"],
                                  client_secret=os.environ["SECRET_KEY"],
                                  user_agent="WebScrapper",
                                  username="PythonScrapper",
                                  password=os.environ["REDDIT_PASSWORD"] )
        self.reddit.read_only = True
        starting_timestamp = 0
        self.json_api = {"data": ["None"]}
        while True:
            url = url_base + f"?subreddit={subreddit}&score=>{score}&after={starting_timestamp}&sort=asc&size=500"
            self.json_api = read_json(url)["data"]
            for submission in self.json_api:
                submission = self.reddit.submission(url=submission["full_link"])
                image = Image(submission)
                image.save()
            if len(self.json_api) <= 0:
                break
            starting_timestamp = int(self.json_api[-1]["created_utc"])


scrapper = WebScrapper()