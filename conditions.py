from numbers import Number
from game_queries import GameQuery


class Condition:
    """
    Conditions are essentially object - value pairs that are to be evaluated either as true or false.
    """

    def __init__(self, key, attribute_path, values, not_=False):
        """
        :param key: String, the key of the condition.
        :param attribute_path: String, The "path" of the attribute of the object that the condition references.
                               The "path" is evaluated as the chain of attributes/keys/indexes which can point
                               to a specific variable (starting from game). Each attribute/key/index in the path
                               is divided by a point "."
        :param values: List of Strings/Booleans/Lists of numbers/Numbers, the values or value ranges for which the
                      condition is deemed True. All the elements of the list are sufficient conditions for
                      valuing the condition as True.
        :param not_: Boolean, default=False, If True, the truth value of each value comparison is reversed.
        """
        self.key = key
        self.attribute_path = attribute_path
        self.values = values
        self.not_ = not_

    def eval_condition(self, game):
        q = GameQuery(game, self.attribute_path)
        path = q.query()
        if not path:
            return False
        for v in self.values:
            res = self.__compare_value(path[-1], v)
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

