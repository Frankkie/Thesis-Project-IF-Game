from game_queries import GameQuery


class StateUpdate:
    """
    The class for changes to the game contained in events.
    """

    def __init__(self, attribute_path, new_value_expression):
        """
        :param attribute_path:
        :param new_value_expression:
        """
        self.attribute_path = attribute_path
        self.new_value_expression = new_value_expression

    def state_update(self, game):
        split_path = self.attribute_path.split(".")
        q = GameQuery(game, self.attribute_path)
        objects = q.query()
        if not objects:
            return None
        old_value = objects[-1]
        obj = objects[-2]
        new_value = self.__eval_expression(old_value)
        self.__custom_setattr(obj, new_value, split_path)
        self.__special_game_state_changes(game, split_path, objects, old_value, new_value)
        return new_value

    def __custom_setattr(self, obj, new_value, path):
        attribute_name = path[-1]
        if type(obj) == dict:
            obj[attribute_name] = new_value
        elif type(obj) == list or type(obj) == tuple:
            obj[int(attribute_name)] = new_value
        else:
            setattr(obj, attribute_name, new_value)

    def __eval_expression(self, x):
        # Step 1
        allowed_names = {"x": x}
        # Step 2
        code = compile(self.new_value_expression, "<string>", "eval")
        # Step 3
        for name in code.co_names:
            if name not in allowed_names:
                # Step 4
                raise NameError(f"Use of {name} not allowed")
        return eval(code, {"__builtins__": {}}, allowed_names)

    def __special_game_state_changes(self, game, path, objects, old_value, new_value):
        first_name = path[-1]
        if first_name == "container":
            contained = objects[-2]
            if new_value in game.rooms.keys():
                container = game.rooms[new_value]
            elif new_value in game.things.keys():
                container = game.things[new_value]
            elif new_value is None:
                container = game.currents['room']
            else:
                container = game.actors[new_value]

            if old_value in game.rooms.keys():
                old_container = game.rooms[old_value]
            elif old_value in game.things.keys():
                old_container = game.things[old_value]
            else:
                old_container = game.actors[old_value]

            old_container -= contained
            container += contained

    def to_json(self):
        """
           convert the instance of this class to json
        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = self.__class__.__name__
        return obj_dict
