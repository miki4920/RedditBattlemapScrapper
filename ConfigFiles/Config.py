from PIL import Image

from UtilityFunctions.FileFunctions import read_json


class ConfigList(object):
    base_url = "http://api.pushshift.io/reddit/search/submission/"
    file_extensions = ["jpg", "png"]
    starting_timestamp = 0

    download_path = "Maps/"
    temporary_path = "Temp/"
    dictionary_path = "maps_dictionary.json"

    image_similarity = 0
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    minimum_tag_repetitions = 5
    black_list_words = open("ConfigFiles/black_list_words.txt", "r").read().split("\n")
    stop_words = open("ConfigFiles/stop_words.txt", "r").read().split("\n")
    subreddits = read_json("ConfigFiles/subreddits.json")
    upload_ip = "http://192.168.0.36/maps/"
    minimum_file_size = 5000
    maximum_file_size = 20485760
    Image.MAX_IMAGE_PIXELS = None


Config = ConfigList()