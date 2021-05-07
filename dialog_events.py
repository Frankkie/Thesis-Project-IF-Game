"""
This file includes the DialogEvent class. DialogEvents are events that are triggered specifically by
Topics.

Classes:
    DialogEvent(Event)

"""


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


