import requests
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder
from UtilityFunctions import read_json, write_json, read_file


def correct_response(response):
    response_code = response.status_code
    if response_code == 200:
        return "remove"


class MapUploader(object):
    def __init__(self, config):
        self.config = config

    def upload_file(self, file):
        try:
            response = requests.post(self.config["upload_ip"], data=file,
                                     headers={'Content-Type': file.content_type})
            return response
        except Exception as e:
            print(e)

    def upload_dictionary(self):
        submissions = read_json(self.config["dictionary_path"])
        temporary_submissions = submissions.copy()
        for submission in temporary_submissions:
            metadata = [('image',
                        (f"{submission['name']}.{submission['extension']}", read_file(submission['path']),
                        f"image/{submission['extension']}")),
                        ("name", "nick"),
                        ("squareWidth", str(submission["width"])),
                        ("squareHeight", str(submission["height"]))] + [("tags", tag) for tag in submission["tags"]]
            file = MultipartEncoder(
                fields=metadata
            )
            response = self.upload_file(file)
            print(response, response.content)
            if response.status_code == 200:
                os.remove(submission["path"])
                submissions.remove(submission)
            elif response.status_code == 400:
                internal_code = str(response.content)[2:4]
                if internal_code == "00":
                    os.remove(submission["path"])
                    submissions.remove(submission)
        write_json(self.config["dictionary_path"], submissions)


