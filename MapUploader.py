import requests
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder
import re


def correct_response(response):
    response_code = re.search("\d{3}", str(response))
    response_content = str(response.content)
    print(response, response_content)
    if response_code:
        response_code = response_code.group(0)
        if response_code == "200":
            return 'remove'
        elif response_code == "400":
            response_code = re.search("\d{2}", response_content).group(0)
            if response_code == "00":
                return 'remove'
            elif response_code == '01':
                return 'remove'
        elif response_code == "500":
            return 'remove'
    quit()
    return False


class MapUploader(object):
    def __init__(self, url, root):
        self.url = url
        self.root = root

    def upload_file(self, file_name, file):
        response = requests.post(self.url, data=file,
                                 headers={'Content-Type': file.content_type})
        response_code = correct_response(response)
        if response_code == 'remove':
            os.remove(self.root + file_name)
        elif response_code == 'retry':
            self.upload_file(file_name, file)

    def upload_dictionary(self, file_dictionary):
        for map_name in file_dictionary:
            file = MultipartEncoder(
                fields=file_dictionary[map_name]
            )
            self.upload_file(map_name, file)

