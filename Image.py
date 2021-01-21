import re
from UtilityFunctions import *


class Image(object):
    def __init__(self, submission):
        self.submission = submission
        self.image_name = None
        self.image = None
        if find_file_extension(self.submission.url) and re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", self.submission.title):
            self.handle_name()
            self.image = request_file(self.submission.url)

    def handle_name(self):
        image_name = self.submission.title.lower()
        image_name = re.sub(r'\W+', '_', image_name)

        image_size = re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", self.submission.title)
        image_name = image_name.replace(image_size.group(0), "_")

        image_name = re.sub(r'[^a-zA-Z_]', '', image_name)
        image_name = filter_words(image_name)
        image_name = re.sub("(_)+", "_", image_name)
        image_name = re.sub("_$|^_", "", image_name)
        self.image_name = image_name + "_" + f"{image_size.group(0)}" + self.submission.url[-4:]

    def save(self):
        if self.image:
            save_file(self.image_name, self.image)



