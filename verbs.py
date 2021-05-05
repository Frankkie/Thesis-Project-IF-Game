"""
Contains the Verb class.

Classes:
    Verb

"""


class Verb:
    """
    The class whose instances represent the possible actions of the game.

    Attributes
    ----------
    None defined here.

    Methods
    -------
    __str__:
        Returns a string representing the object.
    to_json:
        Convert the instance of this class to a serializable object.

    """
    def __init__(self, forms, patterns, name):
        """
        Constructor of the verb class.

        :param forms: List of Strings
            The forms that the verb may appear in player commands.
        :param patterns: List of Strings
            The syntax patterns in which the verb can be used in (either '', 'Q', 'O', 'OQI').
            '' is for an intrasitive verb with no qualifiers.
            'Q' is for an intrasitive verb with a qualifier.
            'O' is for a transitive verb with only direct object(s).
            'OQI' is for a transitive verb with direct and indirect object(s).
        :param name: String
            A unique name to id this verb.

        """
        self.forms = forms
        self.patterns = patterns
        self.name = name

    def __str__(self):
        """
        A string representation of the object.

        :return: String

        """
        return self.name

    def to_json(self):
        """
        Convert the instance of this class to a serializable object.

        :return: Dictionary
            A dictionary of the object's attributes, containing the key '_class_'.

        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = "Verb"
        return obj_dict


