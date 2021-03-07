import requests
import os
from UtilityFunctions import read_json, write_json
from requests_toolbelt.multipart.encoder import MultipartEncoder


def correct_response(response):
    response_code = response.status_code
    if response_code == 200:
        return "remove"


class MapUploader(object):
    def __init__(self, config):
        self.config = config

    def upload_file_python(self, submission):
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
        try:
            response = requests.post(self.config["upload_ip"], data=metadata, files=image)
            return response
        except Exception as e:
            print(e)

    def upload_file_java(self, submission):
        fields = [
                ('image', (submission["name"] + "." + submission["extension"], open(submission["path"], 'rb'), 'image/' + submission["extension"])),
                ('name', 'nick'),
            ]
        if submission["width"]:
            fields.extend([('squareWidth', str(submission["width"])),
                ('squareHeight', str(submission["height"]))])
        fields.extend([("tags", tag) for tag in submission["tags"]])
        multipart_data = MultipartEncoder(
            fields=fields
        )
        try:
            response = requests.post(self.config["upload_ip"], data=multipart_data,
                  headers={'Content-Type': multipart_data.content_type})
            return response
        except Exception as e:
            print(e)

    def upload_dictionary(self):
        submissions = read_json(self.config["dictionary_path"])
        temporary_submissions = submissions.copy()
        for submission in temporary_submissions:
            if "127" in self.config["upload_ip"]:
                response = self.upload_file_python(submission)
            else:
                response = self.upload_file_java(submission)

            if response.status_code:
                if response.status_code == 400 and str(response.content)[2:4] == "01":
                    print(response, response.content)
                    print("Bad Name: " + submission["name"])
        write_json(self.config["dictionary_path"], submissions)
