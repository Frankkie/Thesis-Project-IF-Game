"""
Contains the Room class.

Classes:
    Room(Entity)

"""


from entities import Entity


class Room(Entity):
    """
    The parent Class of all Rooms. A room instance is a component of a Chapter map, and contains
    all the objects available to the player, as well as a set of directions for the player to exit it.]

    Attributes
    ----------
    directions: dict, keys = strings, values = dicts
        Contains the possible directions to exit the room from.

    Methods
    -------
    string(print_parts=True, print_directions=True):
        Returns a string representation of the room.
    __iand__(other):
        Adds another direction to the directions dictionary of the object.

    """
    def __init__(self, *args, directions=None, **kwargs):
        """
        Constructor of Room.

        :param args:
            For the base constructor.
        :param directions: default = None, dict, keys = strings, values = dicts
            Contains the possible directions to exit the room from.
            Keys are directions. Can be either compass directions, up, down, or anything else.
            Values are dictionaries containing:
                'room': The key of the room instance in this direction.
                'desc': A description of the direction.
        :param kwargs:
            For the base constructor.

        """
        super().__init__(*args, **kwargs)
        if not directions:
            self.directions = {}
        else:
            self.directions = directions

    def string(self, print_parts=True, print_directions=True):
        """
        This method returns a string representation of the object.

        :param print_parts: Boolean, Default=True
            if True, it prints the objects in self.parts.
        :param print_directions: Boolean, Default=True
            if True, it prints the objects in self.directions.
        :return: String
            a string describing the object.

        """
        printable = self.display_name + "\n" + self.description + "\n"
        if print_parts:
            for part in self.contents.keys():
                printable += f"- {self.contents[part]['obj'].display_name.capitalize()}:" \
                             f" {self.contents[part]['obj'].description}\n"
            printable += "\n"

        if print_directions:
            for direction in self.directions.keys():
                printable += f"- {direction}: {self.directions[direction]['desc']}\n"
            printable += "\n"

        return printable

    def __iand__(self, other):
        """
        This method adds another direction to the directions dictionary of the object.

        :param other: dictionary,
            "dir" should be a direction string,
            "room" should be a Room instance,
            "desc" should be the directions description (optional)
        :return: Room
            The object itself.

        """
        if isinstance(other, dict):
            if isinstance(other["room"], Room):
                room = other["room"].key
            else:
                raise TypeError

            dir_ = other["dir"]
            if "desc" not in other.keys():
                desc = room.description
            else:
                desc = other["desc"]
        else:
            raise TypeError

        self.directions[dir_] = {"room": room, "desc": desc}
        return self

    def _on_look(self, **kwargs):
        if self.examine_description:
            return f"The {self.display_name}: " + self.examine_description
        elif self.description:
            return f"The {self.display_name}: " + self.string()
        else:
            return f"There is nothing interesting about the {self.display_name}."

    def _on_listen(self, **kwargs):
        if self.audible_description:
            return self.audible_description
        else:
            return f"You don't hear anything interesting in the {self.display_name}."

