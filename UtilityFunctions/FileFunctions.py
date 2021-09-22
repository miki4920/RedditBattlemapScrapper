import json


def write_file(path, content):
    with open(path, "wb") as file:
        file.write(content)


def read_json(path):
    try:
        with open(path, 'r') as file:
            json_object = file.read()
    except FileNotFoundError:
        json_object = json.dumps([])
    return json.loads(json_object)


def write_json(path, content):
    with open(path, 'w') as file:
        json.dump(content, file, indent=4)




