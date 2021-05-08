"""
This file includes the DialogEvent class. DialogEvents are events that are triggered specifically by
Topics.

Classes:
    DialogEvent(Event)

"""


import random

from events import Event


class DialogEvent(Event):
    """
    DialogEvents are events that are triggered specifically by Topics. They can also have extra trigger conditions.

    Attributes:
        args:
            For the base class Event.
        trigger_topic: str
            The key of the Topic Object that may trigger this DialogEvent.
        quips: List of quip.keys (str)
            A list of all the quips that this event may return.
        shuffle_quips: Bool, default False
            If True, the quips in the quips list are shown in a random order.
        kwargs:
            For the base class Event.

    Methods:


    """
    def __init__(self, *args, trigger_topic, quips, shuffle_quips=False, **kwargs):
        """
        The constructor of DialogEvent.

        :param args:
            For the base class Event.
        :param trigger_topic: str
            The key of the Topic Object that may trigger this DialogEvent.
        :param quips: List of quip.keys (str)
            A list of all the quips that this event may return.
        :param shuffle_quips: Bool, default False
            If True, the quips in the quips list are shown in a random order.
        :param kwargs:
            For the base class Event.

        """
        super().__init__(*args, **kwargs)
        self.trigger_topic = trigger_topic
        self.quips = quips
        self.shuffle_quips = shuffle_quips

    def eval_topic_conditions(self, game, topic):
        """
        Evaluating whether or not a DialogEvent can be triggered or not.
        First checks if the topic given matches the event's topic. If it does, it calls
        the base eval_conditions function.

        :param game: Game object
            The game object that calls this DialogEvent.
        :param topic: Topic object
            The topic that is active in the game conversation.
        :return: Boolean

        """
        if topic != self.trigger_topic:
            return False
        return self.eval_conditions(game)

    def get_score(self):
        """
        Get the specificity score of the Event. Here it is one more than the number of its conditions
        (as the topic is effectively itself a condition).

        :return: int
            The number of the Event's conditions.

        """
        return len(self.trigger_conditions) + 1

    def trigger(self, game):
        result = list()
        result.append(self.__pick_quip(game))
        self.done += 1
        self.__change_game_state(game)
        if self.next_event_key:
            res = self.__trigger_next(game)
            if res:
                result += res
        return result

    def __pick_quip(self, game):
        if not self.shuffle_quips:
            for q in self.quips:
                if not q.is_said or q.is_repeatable:
                    return q

        elif self.shuffle_quips:
            random.shuffle(self.quips)
            for q in self.quips:
                if not q.is_said or q.is_repeatable:
                    return q

        return f"Stop asking me about the {game.topics[self.trigger_topic].display_name}!!!"

