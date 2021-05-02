

class Event:
    def __init__(self, key, trigger_conditions=None, game_state_changes=None, event_description="",
                 done=False):
        self.key = key
        if not trigger_conditions:
            trigger_conditions = {}
        self.trigger_conditions = trigger_conditions
        if not game_state_changes:
            game_state_changes = {}
        self.game_state_changes = game_state_changes
        self.event_description = event_description
        self.done = done

    def trigger(self, game):
        result = self.event_description
        self.done = True
        self.__change_game_state(game)
        return result

    def __change_game_state(self, game):
        pass

    def to_json(self):
        """
           convert the instance of this class to json
        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = self.__class__.__name__
        return obj_dict
