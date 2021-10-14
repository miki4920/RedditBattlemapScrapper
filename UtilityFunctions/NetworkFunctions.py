import requests
import time

from Config import CONFIG


def get_api_url(subreddit, timestamp):
    return CONFIG.base_url + f"?subreddit={subreddit}" + f"&after={timestamp}&sort=asc&size=1000"


def request_file(url, timeout=0):
    request = requests.get(url)
    time.sleep(timeout)
    return request
