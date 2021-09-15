import re

from ConfigFiles.Config import Config


def __image_format(submission):
    return submission["url"][-3:] not in Config.file_extensions


def __image_origin(submission):
    return not re.search("i\..*\.it", submission["url"])


def __blacklist(submission):
    image_name = submission["title"].lower()
    return any([word in image_name for word in Config.black_list_words])


def __grid(submission, gridded):
    if not gridded:
        return False
    size = re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", submission["title"])
    return not size


def check_title(submission, gridded):
    if __image_format(submission):
        return False
    if __image_origin(submission):
        return False
    if __blacklist(submission):
        return False
    if __grid(submission, gridded):
        return False
    return True


def check_file_size(submission):
    return Config.minimum_file_size < len(submission) < Config.maximum_file_size

