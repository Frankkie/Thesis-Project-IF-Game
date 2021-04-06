"""
    The Entity Class is the parent of the classes:
        Thing
        Room
        Actor
"""


class Entity:
    def __init__(self, reference_name, reference_noun, display_name, description="",
                 container=None, contents=None, plural=False):
        """
        This is the parent class of all Entities (Things, Rooms, Actors).

        Args:
            :param reference_name: This is the name of the object when referenced internally by the game.
            :param reference_noun: This is the noun by which the object is referenced by the player.
                                   Must be a single word.
            :param display_name: This is the string by which the game displays the object.
            :param description: default="", this is the string by which the object is described by the look method.
            :param container: default=None, this is the container Entity of the object.
            :param contents: default=None, dictionary. The components of this object:
                             {reference_name: [Entity Instance, description]}
            :param plural: False if the object is a single entity, True if it is multiple entities.
        """

        self.reference_name = reference_name
        self.reference_noun = reference_noun
        self.display_name = display_name
        self.description = description
        self.container = container
        if not contents:
            self.contents = {}
        else:
            self.contents = contents
        self.plural = plural

    def __str__(self):

        printable = self.display_name.capitalize() + "\n" + self.description + "\n"
        return printable

    def __iadd__(self, other):

        """
        This method adds another object descended from Entity to this object's self.parts.
        It also updates the other.container to [self.reference_name, self.__class__.__name__].

        :param other: iterable, other[0] should be an Entity instance,
                                other[1] should be the component's description (optional)
        :return: The object itself.
        """
        if isinstance(other, list) or isinstance(other, tuple):
            if isinstance(other[0], Entity):
                obj = other[0]
                obj.container = [self.reference_name, self.__class__.__name__]
                if len(other) == 1:
                    desc = obj.description
                else:
                    desc = other[1]
            else:
                raise TypeError
        else:
            raise TypeError

        self.contents[other[0].reference_name] = [obj, desc]
        return self

    def to_json(self):
        """
           convert the instance of this class to json
        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = self.__class__.__name__
        return obj_dict
