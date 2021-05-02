from entities import Entity


class Thing(Entity):
    def __init__(self, *args, reference_adjectives=None, **kwargs):
        """
        This is the parent class of all inanimate objects.

        Args:
            :param reference_adjectives: default=None, this is a list of adjectives by which the object.
                                         might be referred by the player.
        """
        super().__init__(*args, **kwargs)
        if reference_adjectives is None:
            self.reference_adjectives = []
        else:
            self.reference_adjectives = reference_adjectives

    def string(self, print_parts=True):
        """
        This method returns a string representation of the object.

        :param print_parts: Default=True, if True, it prints the objects in self.parts.
        :return: a string describing the object.
        """
        printable = self.display_name + "\n" + self.description + "\n"
        if print_parts:
            for part in self.contents.keys():
                printable += self.contents[part][1]
                printable += " "
            printable += "\n"

        return printable


