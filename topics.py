"""
This file includes the Topic class. Topics are not Entities, but can be referred to by players
during conversations.

Classes:
    Topic

"""


from errors import DialogError


class Topic:
    """
    Topics are not Entities, but can be referred to by players during conversations.

    Attributes
    ----------
    key: str
        This is the name of the object when referenced internally by the game.
    display_name: str
        This is the string by which the game displays the object.
    reference_noun: str
        This is the noun by which the object is referenced by the player. Must be a single word.
    topic_quip: str
        This is the string that is printed when the topic is invoked.
    actor_key: str
        The key of the actor object that knows about the topic.
    reference_adjectives: list of str, default None
        A list of all the adjectives by which this topic can be referred to in player commands.
    is_active: bool, default True
        True, if the topic is active
    times_invoked: int, default 0
        This attribute increments each time the Topic is invoked.

    Methods
    -------
    to_json:
        Convert the instance of this class to a serializable object.

    """
    def __init__(self, key, display_name, reference_noun, topic_quip, actor_key, reference_adjectives=None,
                 is_active=True, times_invoked=0):
        """
        This is the parent class of all topics.

        :param key: str
            This is the name of the object when referenced internally by the game.
        :param display_name: str
            This is the string by which the game displays the object.
        :param reference_noun: str
            This is the noun by which the object is referenced by the player. Must be a single word.
        :param topic_quip: str
            This is the string that is printed when the topic is invoked.
        :param actor_key: str
            The key of the actor object that knows about the topic.
        :param reference_adjectives: list of str, default None
            A list of all the adjectives by which this topic can be referred to in player commands.
        :param is_active: bool, default True
            True, if the topic is active
        :param times_invoked: int, default 0
            This attribute increments each time the Topic is invoked.

        """
        self.key = key
        self.display_name = display_name
        self.reference_noun = reference_noun
        self.topic_quip = topic_quip
        self.actor_key = actor_key
        if not reference_adjectives:
            reference_adjectives = []
        self.reference_adjectives = reference_adjectives
        self.is_active = is_active
        self.times_invoked = times_invoked

    def on_topic(self, **kwargs):
        game = kwargs['game']

        # The actor Object, not the actor key
        actor = kwargs['actor']
        convonode_key = actor.active_convonode

        try:
            convonode = game.convonodes[self.actor_key][convonode_key]
        except KeyError:
            raise DialogError("ConvoNodeNotFound", convonode=convonode_key)

        try:
            response = convonode.handle_topic(actor, self.key, game)
            result = [self.topic_quip, response]
            return result
        except DialogError as error:
            raise error

    def to_json(self):
        """
        Convert the instance of this class to a serializable object.

        :return: Dictionary
            A dictionary of the object's attributes, containing the key '_class_'.

        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = self.__class__.__name__
        return obj_dict
