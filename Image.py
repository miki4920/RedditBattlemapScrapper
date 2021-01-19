import re
from UtilityFunctions import *

map_format = [".jpg", ".png"]
root = "Maps/"


class Image(object):
    def __init__(self, submission):
        self.submission = submission
        self.image_name = None
        self.image = None
        self.correct = self.check_image()
        if self.correct:
            self.handle_name()
            self.image = request_file(self.submission.url)

    def check_image(self):
        if not find_file_extension(self.submission.url):
            return False
        elif not re.search("(\d+x(\d+)+)", self.submission.title):
            return False
        return True

    def handle_name(self):
        image_name = self.submission.title.replace(" ", "_")
        image_size = re.search("(\d+x(\d+)+)", self.submission.title)
        image_name = image_name.replace(image_size.group(0), "")
        image_name = re.sub(r'\W+', '', image_name)
        if image_name[-1] != "_":
            image_name += "_"
        self.image_name = root + image_name + f"{image_size.group(0)}" + self.submission.url[-4:]

    def save(self):
        if self.correct and not check_if_file_exists(self.image_name):
            print(self.image_name)
            save_file(self.image_name, self.image)



