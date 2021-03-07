import json


def printAll(data):
    for key, val in data.items():
        print(str.format("{0} : {1}", key, data[key]))


def convertStringToDict(data):
    return json.dumps(data)
