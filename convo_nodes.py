"""
This file includes the ConvoNode class. ConvoNodes are nodes of an NPCs conversation tree for a
particular scene.

Classes:
    ConvoNode

"""


class ConvoNode:
    """
    The class implementing the nodes of a conversation tree.

    Attributes:
        key: string
            This is the name of the object when referenced internally by the game.
        next_nodes: dictionary, keys node.keys, values list of topics and conditions
            This dictionary points to other nodes in the conversation tree, along with their triggering topics.
            Some nodes might also have triggering conditions.
        topics: dictionary of topics
            The catalogue of topics available in this conversation node.
        to_generic_allowed: bool, default True
            If true, the node can exit topics other than the ones in its next_nodes dictionary. If this happens,
            the next node will be the generic node.
        generic_not_allowed_desc: string, default empty
            If to_generic_allowed is False, this string will be printed when the player enters a topic not
            satisfying any of the next_nodes' conditions.
        default_quips: list of quips, default None
            Quips printed if no matching topic is invoked.

    Methods:


    """
    def __init__(self, key, next_nodes, topics, to_generic_allowed=True, generic_not_allowed_desc="",
                 default_quips=None):
        """

        :param key: string
            This is the name of the object when referenced internally by the game.
        :param next_nodes: dictionary, keys node.keys, values list of topics and conditions
            This dictionary points to other nodes in the conversation tree, along with their triggering topics.
            Some nodes might also have triggering conditions.
        :param topics: dictionary of topics
            The catalogue of topics available in this conversation node.
        :param to_generic_allowed: bool, default True
            If true, the node can exit topics other than the ones in its next_nodes dictionary. If this happens,
            the next node will be the generic node.
        :param generic_not_allowed_desc: string, default empty
            If to_generic_allowed is False, this string will be printed when the player enters a topic not
            satisfying any of the next_nodes' conditions.
        :param default_quips: list of quips, default None
            Quips printed if no matching topic is invoked.

        """
        self.key = key
        self.next_nodes = next_nodes
        self.topics = topics
        self.to_generic_allowed = to_generic_allowed
        self.generic_not_allowed_desc = generic_not_allowed_desc
        if not default_quips:
            default_quips = []
        self.default_quips = default_quips

    def to_json(self):
        """
        Convert the instance of this class to a serializable object.

        :return: Dictionary
            A dictionary of the object's attributes, containing the key '_class_'.

        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = self.__class__.__name__
        return obj_dict