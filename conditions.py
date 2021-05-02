from numbers import Number
from game_queries import GameQuery


class Condition:
    """
    Conditions are essentially object - value pairs that are to be evaluated either as true or false.
    """

    def __init__(self, key, instance_key, instance_type, attribute_name, values, not_=False):
        """
        :param key: String, the key of the condition.
        :param instance_key: String, the key of the object that the condition references.
        :param instance_type: String, either Thing, Room, Actor or Game.
        :param attribute_name: The name of the attribute of the object that the condition references.
        :param values: List of Strings/Booleans/Lists of numbers/Numbers, the values or value ranges for which the
                      condition is deemed True. All the elements of the list are sufficient conditions for
                      valuing the condition as True.
        :param not_: Boolean, default=False, If True, the truth value of each value comparison is reversed.
        """
        self.key = key
        self.instance_key = instance_key
        self.instance_type = instance_type
        self.attribute_name = attribute_name
        self.values = values
        self.not_ = not_

    def eval_condition(self, game):
        try:
            q = GameQuery(game, self.instance_type, self.instance_key, self.attribute_name)
            obj, attr = q.query()
        except AttributeError:
            print("Attribute not found! ", self.instance_type, self.instance_key, self.attribute_name)
            return False
        for v in self.values:
            res = self.__compare_value(attr, v)
            if self.not_:
                res = not res
            if res:
                return True
        return False

    def __compare_value(self, attribute, value):
        if not value:
            if attribute is None:
                return True
            else:
                return False
        if isinstance(value, Number) or type(value) == str or type(value) == bool:
            return attribute == value
        if isinstance(value, list):
            lower = value[0]
            upper = value[1]
            if not lower:
                return value < upper
            if not upper:
                return value > lower
            else:
                return lower < value < upper

    def to_json(self):
        """
           convert the instance of this class to json
        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = self.__class__.__name__
        return obj_dict

