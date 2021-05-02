

class GameQuery:
    """

    """

    def __init__(self, game, instance_type, instance_key, attribute_name):
        """
        :param instance_key: String, the key of the object that the condition references.
        :param instance_type: String, either Thing, Room, Actor or Game
        :param attribute_name: The name of the attribute of the object that the condition references.
        """
        self.game = game
        self.instance_type = instance_type
        self.instance_key = instance_key
        self.instance_type = instance_type
        self.attribute_name = attribute_name

    def query(self):
        obj = self.__disambiguate_object()
        if not obj:
            raise AttributeError
        try:
            attr = self.__disambiguate_attribute(obj)
        except (KeyError, AttributeError):
            raise AttributeError
        return obj, attr

    def __disambiguate_object(self):
        if self.instance_type == "Game":
            try:
                return getattr(self.game, self.instance_key)
            except AttributeError:
                return None
        if self.instance_type == "Room":
            try:
                return self.game.rooms[self.instance_key]
            except KeyError:
                return None
        if self.instance_type == "Actor":
            try:
                return self.game.actors[self.instance_key]
            except KeyError:
                return None
        else:
            try:
                return self.game.things[self.instance_key]
            except KeyError:
                return None

    def __disambiguate_attribute(self, obj):
        if self.instance_type == "GameState":
            try:
                return obj[self.attribute_name]
            except KeyError:
                raise KeyError
        else:
            try:
                return getattr(obj, self.attribute_name)
            except AttributeError:
                raise AttributeError
