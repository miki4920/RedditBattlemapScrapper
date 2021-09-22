from PIL import Image

from UtilityFunctions.FileFunctions import read_json


class CONFIG(object):
    base_url = "http://api.pushshift.io/reddit/search/submission/"
    file_extensions = {"jpg", "png"}

    download_path = "Maps/"
    temporary_path = "Temp/"
    dictionary_path = "maps_dictionary.json"

    minimum_tag_repetitions = 5
    name_length = 50
    black_list_words_path = "Data/black_list_words.json"
    stop_words_path = "Data/stop_words.json"
    subreddits_path = "Data/subreddits.json"
    upload_ip = "http://127.0.0.1:5000/maps"
    minimum_file_size = 5000
    maximum_file_size = 20485760
    Image.MAX_IMAGE_PIXELS = None
