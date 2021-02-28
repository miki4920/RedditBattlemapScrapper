import requests
import os
from UtilityFunctions import read_json, write_json
import json


def correct_response(response):
    response_code = response.status_code
    if response_code == 200:
        return "remove"


class MapUploader(object):
    def __init__(self, config):
        self.config = config

    def upload_file(self, image, metadata):
        try:
            response = requests.post(self.config["upload_ip"], data=metadata, files=image)
            return response
        except Exception as e:
            print(e)

    def upload_dictionary(self):
        submissions = read_json(self.config["dictionary_path"])
        temporary_submissions = submissions.copy()
        for submission in temporary_submissions:
            image = {"picture": open(submission["path"], "rb")}
            if len(submission["tags"]) > 1:
                submission["tags"] = ",".join(submission["tags"])
            metadata = {"name": submission["name"],
                        "extension": submission["extension"],
                        "uploader": "nick",
                        "square_width": submission["width"],
                        "square_height": submission["height"],
                        "tags": submission["tags"]
                        }

            response = self.upload_file(image, metadata)
            if response.status_code == 200:
                os.remove(submission["path"])
                submissions.remove(submission)
            elif response.status_code == 400:
                internal_code = str(response.content)[2:4]
                if internal_code == "00":
                    os.remove(submission["path"])
                    submissions.remove(submission)
                elif internal_code == "01":
                    print(f"Bad Name: {submission['name']}")
            else:
                print(response, response.content)
        write_json(self.config["dictionary_path"], submissions)
