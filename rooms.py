from entities import Entity


class Room(Entity):
    def __init__(self, *args, directions=None, **kwargs):
        """
            Descended from Entity.
            Additional arguments:
                :param directions: default=None, dictionary. The directions of this Room object:
                                  {direction: [Entity Instance, description]}
        """
        super().__init__(*args, **kwargs)
        if not directions:
            self.directions = {}
        else:
            self.directions = directions

    def string(self, print_parts=True, print_directions=True):
        """
        This method returns a string representation of the object.
        :param print_parts: Default=True, if True, it prints the objects in self.parts.
        :param print_directions: Default=True, if True, it prints the objects in self.directions.
        :return: a string describing the object.

        """
        printable = self.display_name + "\n" + self.description + "\n"
        if print_parts:
            for part in self.contents.keys():
                printable += self.contents[part][1]
                printable += " "
            printable += "\n"

        if print_directions:
            for part in self.directions.keys():
                printable += part
                printable += ": "
                printable += self.directions[part][1]
                printable += " "
            printable += "\n"

        return printable

    def __iand__(self, other):
        """
            This method adds another direction to the directions dictionary of the object.

            :param other: iterable, other[0] should be a direction string,
                                    other[1] should be an Entity instance,
                                    other[2] should be the directions description (optional)
            :return: The object itself.
        """
        if isinstance(other, list) or isinstance(other, tuple):
            if isinstance(other[1], Entity):
                obj = other[1]
                dir_ = other[0]
                obj.container = [self.reference_name, self.__class__.__name__]
                if len(other) == 2:
                    desc = obj.description
                else:
                    desc = other[2]
            else:
                raise TypeError
        else:
            raise TypeError

        self.directions[dir_] = [obj, desc]
        return self

