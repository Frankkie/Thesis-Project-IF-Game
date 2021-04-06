from verbs import *
from rooms import *
from things import *

import json


class EncodeCustom(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entity):
            return obj.to_json()
        if isinstance(obj, Verb):
            return obj.to_json()
        return json.JSONEncoder.default(self, obj)


def custom_dump(dictionary, json_file):
    with open(json_file, "w") as file:
        json.dump(dictionary, file, cls=EncodeCustom, indent=4)


class DecodeCustom(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if isinstance(dct, dict) and '_class_' in dct:
            class_name = dct['_class_']
            del dct['_class_']
            get_class = lambda x: globals()[x]
            cl = get_class(class_name)
            return cl(**dct)
        return dct


def custom_load(json_file):
    with open(json_file, "r") as file:
        return json.load(file, cls=DecodeCustom)



