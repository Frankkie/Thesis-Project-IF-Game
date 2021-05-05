"""
Serialize and deserialize the custom Objects used in the game.

Classes:
    EncodeCustom(json.JSONEncoder)
    DecodeCustom(json.JSONDecoder)

Functions:
    custom_dump(dictionary, json_file_path):
        Dump dictionary containing custom game Objects to the file indicated by json_file_path.
    custom_load(json_file_path):
        Load data containing custom game Objects to the file indicated by json_file_path.

"""


import json

from verbs import Verb
from entities import Entity
from rooms import Room
from things import Thing
from actors import Actor
from chapters import *
from events import Event
from conditions import Condition
from state_updates import StateUpdate


class EncodeCustom(json.JSONEncoder):
    """
    Encode custom game object to an object serializable by the JSONEncoder.

    Attributes:
        Attributes inherited by the json.JSONEncoder Class.

    Methods (defined here):
        default(obj):
            Overrides the default json.JSONEncoder method. Encodes custom objects
            into dictionaries containing their attributes.

    """
    def default(self, obj):
        """
        Overrides the default json.JSONEncoder method. Encodes custom objects
        into dictionaries containing their attributes. If the object is not custom,
        it calls the base default method.

        :param obj: Object
            The object to be encoded.
        :return:
            A serializable representation of the object.

        """
        if isinstance(obj, Entity):
            return obj.to_json()
        if isinstance(obj, Verb):
            return obj.to_json()
        if isinstance(obj, Chapter):
            return obj.to_json()
        if isinstance(obj, Event):
            return obj.to_json()
        if isinstance(obj, Condition):
            return obj.to_json()
        if isinstance(obj, StateUpdate):
            return obj.to_json()
        return json.JSONEncoder.default(self, obj)


def custom_dump(dictionary, json_file_path):
    """
    Dump dictionary containing custom game Objects to the file indicated by json_file_path.

    :param dictionary: Dictionary
        Contains custom game objects.
    :param json_file_path: String
        The path to the json file where the dictionary is dumped.
    :return: None.

    """
    with open(json_file_path, "w") as file:
        json.dump(dictionary, file, cls=EncodeCustom, indent=4)


class DecodeCustom(json.JSONDecoder):
    """
    Encode custom game object.

    Attributes:
        *args
            for the base class json.JSONDecoder
        **kwargs
            for the base class json.JSONDecoder

    Methods (defined here):
        object_hook(dct):
            Deserialize custom game Object given as a dictionary.

    """
    def __init__(self, *args, **kwargs):
        """
        Constructor, calls the constructor of the base class.

        :param args:
            for the base class json.JSONDecoder
        :param kwargs:
            for the base class json.JSONDecoder

        """
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        """
        Deserialize custom game Object given as a dictionary.
        All custom object that may be deserialized are imported into the module,
        thus making them available into the globals() dictionary. Based on the
        _class_ key given in the serialized custom objects' dictionary, the
        method returns the corresponding object.

        If the object is not custom, the function returns it is.
        :param obj:
            Object to be deserialized.
        :return:
            The deserialized obj.

        """
        if isinstance(obj, dict) and '_class_' in obj:
            class_name = obj['_class_']
            del obj['_class_']
            get_class = lambda x: globals()[x]
            cl = get_class(class_name)
            return cl(**obj)
        return obj


def custom_load(json_file_path):
    """
    Load data containing custom game Objects to the file indicated by json_file_path.

    :param json_file_path: String
        The path to the json file where the dictionary is loaded from.
    :return:
        None

    """
    with open(json_file_path, "r") as file:
        return json.load(file, cls=DecodeCustom)



