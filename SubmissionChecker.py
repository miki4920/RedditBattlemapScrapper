import re

from HashFunctions import hash_distance


class SubmissionChecker(object):
    def __init__(self, config):
        self.config = config

    def image_format(self, submission):
        return submission["url"][-3:] not in self.config["file_extensions"]

    @staticmethod
    def image_origin(submission):
        return not re.search("i\..*\.it", submission["url"])

    def blacklist(self, submission):
        image_name = submission["title"].lower()
        return any([word in image_name for word in self.config["black_list_words"]])

    @staticmethod
    def grid(submission, grid):
        if not grid:
            return False
        size = re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", submission["title"])
        return not size

    def check_title(self, submission, grid):
        if self.image_format(submission):
            return False
        if self.image_origin(submission):
            return False
        if self.blacklist(submission):
            return False
        if self.grid(submission, grid):
            return False
        return True

    def check_file_size(self, submission):
        return self.config["minimum_file_size"] < len(submission) < self.config["maximum_file_size"]

    def check_hash(self, submission, submission_list):
        for existing_submission in submission_list:
            if hash_distance(submission, existing_submission["hash"]) <= self.config["image_similarity"]:
                return False
        return True
