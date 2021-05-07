"""
This file includes the ConvoNode class. ConvoNodes are nodes of an NPCs conversation tree for a
particular scene.

Classes:
    ConvoNode

"""


class ConvoNode:
    def __init__(self, key):
        self.key = key

    def to_json(self):
        """
        Convert the instance of this class to a serializable object.

        :return: Dictionary
            A dictionary of the object's attributes, containing the key '_class_'.

        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = self.__class__.__name__
        return obj_dict