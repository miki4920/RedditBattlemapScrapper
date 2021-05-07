import requests
import time

from ConfigFiles.Config import Config


def get_api_url(subreddit, timestamp):
    return Config.base_url + f"?subreddit={subreddit}" \
                             f"&score=>{Config.subreddits[subreddit]['score']}" \
                             f"&after={timestamp}&sort=asc&size=1000"


def request_file(url, timeout=0):
    request = requests.get(url, headers=Config.headers)
    time.sleep(timeout)
    return request