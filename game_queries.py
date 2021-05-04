

class GameQuery:
    """

    """

    def __init__(self, game, attribute_path):
        """
        :param attribute_path: String, The "path" of the attribute of the object that the condition references.
                               The "path" is evaluated as the chain of attributes/keys/indexes which can point
                               to a specific variable (starting from game). Each attribute/key/index in the path
                               is divided by a point "."
        """
        self.game = game
        self.attribute_path = attribute_path.split(".")

    def query(self):
        attribute_sequence = [self.game]
        for attr in self.attribute_path:
            deepest_obj = attribute_sequence[-1]
            if type(deepest_obj) == dict:
                try:
                    next_obj = deepest_obj[attr]
                except KeyError:
                    return None
            elif type(deepest_obj) == list or type(deepest_obj) == tuple:
                try:
                    next_obj = deepest_obj[int(attr)]
                except IndexError:
                    return None
            else:
                try:
                    next_obj = getattr(deepest_obj, attr)
                except AttributeError:
                    return None

            attribute_sequence.append(next_obj)
        return attribute_sequence
