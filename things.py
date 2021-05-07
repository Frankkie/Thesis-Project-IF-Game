"""
Contains the Thing class.

Classes:
    Thing(Entity)

"""


from entities import Entity


class Thing(Entity):
    """
    The parent class of all Things. Things in the game are inanimate Entities that are not Rooms
    (meaning that an Actor cannot go inside of them).

    Attributes
    ----------
    reference_adjectives: list of string, default None
        The adjectives by which the player can refer to the object in commands.

    Methods
    -------
    string(print_parts=True):
        Returns a string representing the object.

    """
    def __init__(self, *args, reference_adjectives=None, **kwargs):
        """
        The constructor of Thing.

        :param args:
            For the base constructor.
        :param reference_adjectives: list of string, default None
            The adjectives by which the player can refer to the object in commands.
        :param kwargs:
            For the base constructor.

        """
        super().__init__(*args, **kwargs)
        if reference_adjectives is None:
            self.reference_adjectives = []
        else:
            self.reference_adjectives = reference_adjectives

    def string(self, print_parts=True):
        """
        This method returns a string representation of the object.

        :param print_parts: Boolean, Default=True
            if True, it prints the objects in self.parts.
        :return: String
            a string describing the object.

        """
        printable = self.display_name + "\n" + self.description + "\n"
        if print_parts:
            for part in self.contents.keys():
                printable += self.contents[part]['obj']
                printable += " "
            printable += "\n"

        return printable


