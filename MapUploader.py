import requests
from UtilityFunctions.FileFunctions import read_json, write_json
from ConfigFiles.Config import Config


class MapUploader(object):
    def upload_file(self, submission):
        image = {"picture": open(submission["path"], "rb")}
        if len(submission["tags"]) > 1:
            submission["tags"] = ",".join(submission["tags"])
        metadata = {"name": submission["name"].capitalize(),
                    "extension": submission["extension"],
                    "uploader": "nick",
                    "square_width": submission["width"],
                    "square_height": submission["height"],
                    "tags": submission["tags"]
                    }
        try:
            request = requests.post(Config.upload_ip, data=metadata, files=image)
            return request
        except Exception as e:
            print(e)

    def upload_dictionary(self):
        submissions = read_json(Config.dictionary_path)
        temporary_submissions = submissions.copy()
        for submission in temporary_submissions:
            response = self.upload_file(submission)
            if isinstance(response, requests.Response) and response.status_code == 400:
                print(response.content)
