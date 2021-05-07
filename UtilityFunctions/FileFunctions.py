import json
import os
from pathlib import Path


def write_file(path, content):
    directory = os.path.dirname(path)
    Path(directory).mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as file:
        file.write(content)


def read_json(path):
    if not os.path.exists(path):
        with open(path, 'w') as file:
            json.dump([], file, indent=4)
    with open(path, 'rb') as file:
        json_object = file.read()
    return json.loads(json_object)


def write_json(path, content):
    with open(path, 'w') as file:
        json.dump(content, file, indent=4)




