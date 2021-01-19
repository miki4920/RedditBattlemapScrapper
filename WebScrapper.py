import os
import praw
import requests
import time
from ClientSecrets import token

token()

root = "Maps/"
subreddit = "battlemaps"
map_format = [".png", ".jpg"]


class WebScrapper(object):
    def __init__(self):
        self.reddit = praw.Reddit(client_id=os.environ["CLIENT_ID"],
                                  client_secret=os.environ["SECRET_KEY"],
                                  user_agent="WebScrapper",
                                  username="PythonScrapper",
                                  password=os.environ["REDDIT_PASSWORD"] )
        self.subreddit = self.reddit.subreddit(subreddit)
        for submission in self.subreddit.top(limit=1000):
            image_url = submission.url
            if self.check_image(image_url):
                image_name = self.handle_name(submission)
                image = self.request_image(image_url)
                self.save_image(image, image_name)
            time.sleep(1)

    @staticmethod
    def request_image(image_url):
        image = requests.get(image_url).content
        return image

    @staticmethod
    def check_image(image_url):
        return image_url[-4:] in map_format

    @staticmethod
    def handle_name(submission):
        image_name = submission.title.replace(" ", "_") + submission.url[-4:]
        return image_name

    @staticmethod
    def save_image(image, image_name):
        path = root+image_name
        with open(path, "wb") as file:
            file.write(image)



scrapper = WebScrapper()