"""
This file includes the ConvoNode class. ConvoNodes are nodes of an NPCs conversation tree for a
particular scene.

Classes:
    ConvoNode

"""


from errors import DialogError


class ConvoNode:
    """
    The class implementing the nodes of a conversation tree.

    Attributes:
        key: string
            This is the name of the object when referenced internally by the game.
        next_nodes: dictionary, keys node.keys, values list of topics and conditions
            This dictionary points to other nodes in the conversation tree, along with their triggering topics.
            Some nodes might also have triggering conditions.
        to_generic_allowed: bool, default True
            If true, the node can exit topics other than the ones in its next_nodes dictionary. If this happens,
            the next node will be the generic node.
        generic_not_allowed_desc: string, default empty
            If to_generic_allowed is False, this string will be printed when the player enters a topic not
            satisfying any of the next_nodes' conditions.

    Methods:


    """
    def __init__(self, key, actor, next_nodes, to_generic_allowed=True, generic_not_allowed_desc="",
                 switch_to_generic_desc=''):
        """

        :param key: string
            This is the name of the object when referenced internally by the game.
        :param actor: string
            The key of the actor that the convonode object belongs to.
        :param next_nodes: dictionary, keys: node.keys, values: list of topic keys
            This dictionary points to other nodes in the conversation tree, along with their triggering topics.
            Some nodes might also have triggering conditions.
        :param to_generic_allowed: bool, default True
            If true, the node can exit with topics other than the ones in its next_nodes dictionary. If this happens,
            the next node will be the generic node.
        :param generic_not_allowed_desc: string, default empty
            If to_generic_allowed is False, this string will be printed when the player enters a topic not
            satisfying any of the next_nodes' conditions.
        :param switch_to_generic_desc: string, default empty
            the message printed when switching to the generic node.

        """
        self.key = key
        self.actor = actor
        self.next_nodes = next_nodes
        self.to_generic_allowed = to_generic_allowed
        self.generic_not_allowed_desc = generic_not_allowed_desc
        self.switch_to_generic_desc = switch_to_generic_desc

    def handle_topic(self, actor, topic_key, game):

        next_node = self.switch_node(topic_key)
        print(self.key, next_node)
        if not next_node:
            return [self.generic_not_allowed_desc]

        response = list()
        if self.switch_to_generic_desc and next_node == 'generic':
            response.append(self.switch_to_generic_desc)

        actor.active_convonode = next_node
        try:
            response += self.trigger_dialogevent(actor, topic_key, game, next_node)
        except DialogError as error:
            raise error

        return response

    def trigger_dialogevent(self, actor, topic, game, next_node):
        max_score = 0
        triggered_event = None

        for d_event in game.dialogevents.values():
            if d_event.eval_topic_conditions(game, topic, next_node):
                event_score = d_event.get_score()
                if event_score > max_score:
                    max_score = event_score
                    triggered_event = d_event

        if triggered_event:
            result = triggered_event.trigger(game)
            return result
        else:
            actor_name = actor.display_name
            raise DialogError("NoEventForTopic", actor=actor_name)

    def switch_node(self, topic):
        """
        Find the next node in an actor's conversation tree.
        If the topic given in not in any of the next_nodes conditions,
        then go to the generic node, if to_generic_allowed, or return None is
        to_generic_allowed is False.
        If the next node has an empty list of topics, then any topic will
        trigger the next_node.

        :param topic: str
            the key of the topic invoked
        :return: str or None
            None if there is no other node to go to.
        """
        next_node = None

        for node in self.next_nodes.keys():
            exit_topics = self.next_nodes[node]
            if not exit_topics:
                next_node = node
            if topic in exit_topics:
                next_node = node
                break
            else:
                pass

        if not next_node:
            if self.to_generic_allowed:
                next_node = 'generic'
            else:
                pass

        return next_node

    def to_json(self):
        """
        Convert the instance of this class to a serializable object.

        :return: Dictionary
            A dictionary of the object's attributes, containing the key '_class_'.

        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = self.__class__.__name__
        return obj_dict