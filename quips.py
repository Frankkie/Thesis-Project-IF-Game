"""
This file includes the Quip class. Quips are responses given by NPCs, when responding to a
DialogEvent.

Classes:
    Quip

"""


class Quip:
    """


    Attributes:
        key: str
            This is the name of the object when referenced internally by the game.
        text: str
            The text printed when this quip is returned by a DialogEvent.
        is_said: bool, default False
            True if this quip has been said before.
        is_repeatable: bool, default False
            True if this quip can be said more than once.

    Methods:


    """
    def __init__(self, key, text, is_said=False, is_repeatable=False):
        """
        Constructor of Quip Class.

        :param key: str
            This is the name of the object when referenced internally by the game.
        :param text: str
            The text printed when this quip is returned by a DialogEvent.
        :param is_said: bool, default False
            True if this quip has been said before.
        :param is_repeatable: bool, default False
            True if this quip can be said more than once.

        """
        self.key = key
        self.text = text
        self.is_said = is_said
        self.is_repeatable = is_repeatable

    def to_json(self):
        """
        Convert the instance of this class to a serializable object.

        :return: Dictionary
            A dictionary of the object's attributes, containing the key '_class_'.

        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = self.__class__.__name__
        return obj_dict
