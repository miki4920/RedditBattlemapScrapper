import requests
from UtilityFunctions.FileFunctions import read_json
from Config import CONFIG


class MapUploader(object):
    @staticmethod
    def upload_file(submission):
        submission["tags"] = ",".join(submission["tags"]) if submission["tags"] else None
        image = {"image": open(submission["path"], "rb")}
        try:
            request = requests.post(CONFIG.upload_ip, data=submission, files=image)
            return request
        except requests.exceptions.ConnectionError:
            print("Server Not Online")

    def upload_dictionary(self):
        submissions = read_json(CONFIG.dictionary_path)
        temporary_submissions = submissions.copy()
        for submission in temporary_submissions:
            response = self.upload_file(submission)
            if isinstance(response, requests.Response) and response.status_code in (400, 500):
                print(response.content)
