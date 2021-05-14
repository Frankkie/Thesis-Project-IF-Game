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
    def __init__(self, *args, reference_adjectives=None, is_known=False, **kwargs):
        """
        The constructor of Thing.

        :param args:
            For the base constructor.
        :param reference_adjectives: list of string, default None
            The adjectives by which the player can refer to the object in commands.
        :param is_known: bool, default: False
            True if the Thing can be interacted with by the player.
        :param kwargs:
            For the base constructor.

        """
        super().__init__(*args, **kwargs)

        self.is_known = is_known
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
        printable = str(self)

        try:
            opened = self.entity_state["Open"]
        except KeyError:
            opened = False

        if print_parts:
            for part in self.contents.values():
                if "Look" in part['tags'] and not ('In' in part['tags']):
                    printable += f"- {part['obj'].display_name.capitalize()}:" \
                                 f" {part['obj'].description}\n"

                if "In" in part["tags"] and opened:
                    printable += f"- {part['obj'].display_name.capitalize()}:" \
                                 f" {part['obj'].description}\n"

        return printable


