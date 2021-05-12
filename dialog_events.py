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
        trigger_topics: list of str
            The keys of the Topic Objects that may trigger this DialogEvent.
        quips: List of Quips
            A list of all the quips that this event may return.
        trigger_convonode: str, default None
            the key of the convonode that can trigger the event. If None, all convonodes can trigger this event.
        shuffle_quips: Bool, default False
            If True, the quips in the quips list are shown in a random order.
        kwargs:
            For the base class Event.

    Methods:


    """
    def __init__(self, *args, trigger_topics, quips, trigger_convonode=None, shuffle_quips=False, **kwargs):
        """
        The constructor of DialogEvent.

        :param args:
            For the base class Event.
        :param trigger_topic: list of str
            The keys of the Topic Objects that may trigger this DialogEvent.
        :param quips: List of quip.keys (str)
            A list of all the quips that this event may return.
        :param trigger_convonode: str, default None
            the key of the convonode that can trigger the event. If None, all convonodes can trigger this event.
        :param shuffle_quips: Bool, default False
            If True, the quips in the quips list are shown in a random order.
        :param kwargs:
            For the base class Event.

        """
        super().__init__(*args, **kwargs)
        self.trigger_topics = trigger_topics
        self.quips = quips
        self.trigger_convonode = trigger_convonode
        self.shuffle_quips = shuffle_quips

    def eval_topic_conditions(self, game, topic, convonode):
        """
        Evaluating whether or not a DialogEvent can be triggered or not.
        First checks if the topic given matches the event's topic. If it does, it calls
        the base eval_conditions function.

        :param game: Game object
            The game object that calls this DialogEvent.
        :param topic: Topic object.key
            The key of the topic that is active in the game conversation.
        :return: Boolean

        """
        if topic not in self.trigger_topics:
            return False
        if self.trigger_convonode:
            if convonode != self.trigger_convonode:
                return False

        return self.eval_conditions(game)

    def get_score(self):
        """
        Get the specificity score of the Event. Here it is one more than the number of its conditions
        (as the topic is effectively itself a condition).

        :return: int
            The number of the Event's conditions.

        """
        score = len(self.trigger_conditions) + 1
        if self.trigger_convonode:
            score += 1

        return score

    def trigger(self, game):
        result = list()
        result.append(self.__pick_quip(game))
        self.done += 1
        self._change_game_state(game)
        if self.next_event_key:
            res = self._trigger_next(game)
            if res:
                result += res
        return result

    def __pick_quip(self, game):
        if not self.shuffle_quips:
            for q in self.quips:
                if not q.is_said or q.is_repeatable:
                    q.is_said = True
                    return q.text

        elif self.shuffle_quips:
            random.shuffle(self.quips)
            for q in self.quips:
                if not q.is_said or q.is_repeatable:
                    q.is_said = True
                    return q.text

        return f"'Stop asking me about the {game.topics[self.trigger_topics[0]].display_name}!!!'"

