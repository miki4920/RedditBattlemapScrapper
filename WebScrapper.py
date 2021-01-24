from UtilityFunctions import *
import os
import re


subreddit = "battlemaps"
minimum_submission_score = 100
starting_timestamp = 0
download_directory = "Maps/"
gridded_only = True
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
              'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
              'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these',
              'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
              'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
              'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
              'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
              'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
              'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
              'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'map', 'battlemap', 'battle',
              'oc', 'free', 'ocart', 'comments', 'gridless', 'grid', 'made', 'battlemapoc', 'inspired', 'level',
              'storey', 'three', 'maps', 'feedback', 'handdrawn', 'part', 'px', 'xpx', 'art', 'info', 'one', 'two',
              'three', 'roll', 'virtual', 'version', 'multi', 'original', 'mine', 'four', 'five', 'ppi', 'square',
              'small', 'multi', 'jpg', 'png', 'inktober', 'scale', 'first', 'units', 'grand', 'assets', 'mapvember',
              'floor', 'great', 'rpg', 'battlemaps']


def check_submission(submission):
    if "preview" not in submission.keys():
        return False
    if gridded_only and not get_size(submission["title"]):
        return False
    return True


def filter_words(name):
    name_list = []
    for word in name.split("_"):
        if len(word) < 3:
            pass
        elif word in stop_words:
            pass
        elif word in name_list:
            pass
        else:
            name_list.append(word)
    return "_".join(name_list)


def simplify_name(name):
    name = name.lower()

    name = re.sub(r'[^a-zA-Z_]', '_', name)
    name = filter_words(name)
    name = re.sub("(_)+", "_", name)
    name = re.sub("_$|^_", "", name)
    return name


def get_url(submission):
    submission = submission["preview"]["images"][0]["source"]["url"]
    url = submission.split("?")[0]
    return url


def get_extension(url):
    return url[-3:]


def get_path(name, extension):
    path = download_directory + name + "." + extension
    count = 2
    while os.path.exists(path):
        path = download_directory + name + f"_{count}" + "." + extension
        count += 1
    return download_directory + name + "." + extension


def get_size(image_name):
    size = re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", image_name)
    return size.group(0) if size else False


def create_submission_dictionary(submission):
    name = simplify_name(submission["title"])
    url = get_url(submission)
    extension = get_extension(url)
    path = get_path(name, extension)
    width, height = None, None
    if get_size(submission["title"]):
        width, height = list(map(int, get_size(submission["title"]).split("x")))
    submission_dictionary = {"name": name,
                             "url": url,
                             "extension": extension,
                             "path": path,
                             "width": width,
                             "height": height,
                             "tags": ()
                             }
    return submission_dictionary


def start_scrapping():
    timestamp = starting_timestamp
    submission_list = []
    while True:
        url = "http://api.pushshift.io/reddit/search/submission/" + f"?subreddit={subreddit}&score=>{minimum_submission_score}&after={timestamp}&sort=asc&size=500"
        json_api = list(read_json(url).values())[0]
        for submission in json_api:
            if check_submission(submission):
                submission_dictionary = create_submission_dictionary(submission)
                file = request_file(submission_dictionary["url"])
                print(submission_dictionary["width"], submission_dictionary["height"])
                save_file(submission_dictionary["path"], file)
                submission_list.append(submission_dictionary)
        if len(json_api) < 1:
            break
        timestamp = int(json_api[-1]["created_utc"])


start_scrapping()
