"""
Contains the Thing class and its child classes.

Classes:
    Thing(Entity)
    Fixture(Thing)
    OpenableContainer(Thing)
    Surface(Thing)

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


class Fixture(Thing):
    """
    Fixtures are immovable and unopenable objects.
    """
    def __init__(self, *args, **kwargs):
        try:
            if not kwargs['as_dirobj']:
                kwargs['as_dirobj'] = {}
        except KeyError:
            kwargs['as_dirobj'] = {}

        try:
            if not kwargs['as_indobj']:
                kwargs['as_indobj'] = {}
        except KeyError:
            kwargs['as_indobj'] = {}

        as_indobj = {**kwargs['as_indobj'], **{'On': False, 'In': False, "Under": False}}
        as_dirobj = {**kwargs['as_dirobj'], **{"Look": True, "Take": False, "Drop": False, "Open": False,
                                               "Close": False, "Push": False, "Use": False, "Put": False, "Send": False,
                                               "Landon": False, "Enter": False, "Leave": False, "Setup": False,
                                               "Swerveoff": False}}

        kwargs['as_dirobj'] = as_dirobj
        kwargs['as_indobj'] = as_indobj
        super().__init__(*args, **kwargs)


class OpenableContainer(Thing):
    """
    Openable Containers are openable objects.
    """

    def __init__(self, *args, **kwargs):
        try:
            if not kwargs['as_dirobj']:
                kwargs['as_dirobj'] = {}
        except KeyError:
            kwargs['as_dirobj'] = {}

        try:
            if not kwargs['as_indobj']:
                kwargs['as_indobj'] = {}
        except KeyError:
            kwargs['as_indobj'] = {}

        as_indobj = {**kwargs['as_indobj'], **{'In': True}}
        as_dirobj = {**kwargs['as_dirobj'], **{"Look": True, "Open": True, "Close": True}}
        kwargs['as_dirobj'] = as_dirobj
        kwargs['as_indobj'] = as_indobj
        super().__init__(*args, **kwargs)


class Surface(Thing):
    """
    Surfaces are objects that can be used to lay another object upon.
    """

    def __init__(self, *args, **kwargs):
        try:
            if not kwargs['as_dirobj']:
                kwargs['as_dirobj'] = {}
        except KeyError:
            kwargs['as_dirobj'] = {}

        try:
            if not kwargs['as_indobj']:
                kwargs['as_indobj'] = {}
        except KeyError:
            kwargs['as_indobj'] = {}

        as_indobj = {**kwargs['as_indobj'], **{'On': True}}
        as_dirobj = {**kwargs['as_dirobj'], **{"Look": True, "Open": True, "Close": True}}

        kwargs['as_dirobj'] = as_dirobj
        kwargs['as_indobj'] = as_indobj
        super().__init__(*args, **kwargs)


class Movable(Thing):
    """
    Movables are movable objects.
    """
    def __init__(self, *args, **kwargs):
        try:
            if not kwargs['as_dirobj']:
                kwargs['as_dirobj'] = {}
        except KeyError:
            kwargs['as_dirobj'] = {}

        as_dirobj = {**kwargs['as_dirobj'], **{"Look": True, "Take": True, "Drop": True, "Put": True}}
        kwargs['as_dirobj'] = as_dirobj

        super().__init__(*args, **kwargs)






