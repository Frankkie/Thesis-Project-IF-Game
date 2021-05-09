

class Event:
    def __init__(self, key, trigger_conditions=None, game_state_changes=None, event_description="",
                 done=0, repeatable=True, next_event_key=None):
        self.key = key
        if not trigger_conditions:
            trigger_conditions = []
        self.trigger_conditions = trigger_conditions
        if not game_state_changes:
            game_state_changes = []
        self.game_state_changes = game_state_changes
        self.event_description = event_description
        self.done = done
        self.repeatable = repeatable
        self.next_event_key = next_event_key

    def trigger(self, game):
        result = list()
        result.append(self.event_description)
        self.done += 1
        self.__change_game_state(game)
        if self.next_event_key:
            res = self.__trigger_next(game)
            if res:
                result += res
        return result

    def eval_conditions(self, game):
        if self.repeatable is True:
            pass
        else:
            if self.done >= self.repeatable:
                return False
        for cond in self.trigger_conditions:
            if not cond.eval_condition(game):
                return False
        return True

    def get_score(self):
        """
        Get the specificity score of the Event (number of conditions).

        :return: int
            The number of the Event's conditions.

        """
        return len(self.trigger_conditions)

    def __change_game_state(self, game):
        for state_update in self.game_state_changes:
            state_update.state_update(game)

    def __trigger_next(self, game):
        events = game.events
        try:
            next_event = events[self.next_event_key]
        except KeyError:
            return None
        else:
            result = next_event.trigger(game)
        return result

    def to_json(self):
        """
           convert the instance of this class to json
        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = self.__class__.__name__
        return obj_dict
