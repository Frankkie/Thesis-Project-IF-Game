"""
The module of the Actor class and its subclasses.

Classes:
    Actor(Entity)

"""

from entities import Entity
import json


class Actor(Entity):
    """
    This is the parent class of all Actors. Actors represent the PC and the NPCs of the game.

    Attributes:
        The attributes inherited by Entity.
        abilities: Dict
            The Verbs whose actions this actor can perform.
        on_command: Dict
            The Verbs whose actions this actor can be commanded to perform.

    Methods:
        _on_go(**kwargs)
            Triggered by the Go Verb. Changes the Actor's room.

    """
    def __init__(self, *args, abilities=None, on_command=None, **kwargs):
        """
        The constructor of actors.
        :param args:
            arguments passed to the Entity constructor
        :param abilities: dict
            keys: verb names, values: boolean, depending on whether or not this actor can perform this action.
        :param on_command: dict
            keys: verb names, values: boolean, depending on whether or not this actor can be currently commanded
            to perform this action.
        :param kwargs:
            keyword arguments passed to the Entity constructor
        """
        super().__init__(*args, **kwargs)

        with open("Grammar/verbs.json", "r") as file:
            verbs = json.load(file)  # Load dict of all verbs
        file.close()
        for q in verbs.keys():
            verbs[q] = False

        if not abilities:
            self.abilities = verbs
        else:
            # Set the abilities not given to the method as False
            self.abilities = {**verbs, **abilities}

        if not on_command:
            self.on_command = verbs
        else:
            # Set the commands not given to the method as False
            self.on_command = {**verbs, **on_command}

    def _on_go(self, **kwargs):
        """
        Triggered by the Go verb.
        Changes the actor's room depending on the qualifier (direction) given.

        :param kwargs:
            Keyword args should include 'game', 'qualifier' and 'actor'
        :return: str
            Either the direction description of the new room (if the actor is the PC)
            or a generic result string (if NPC)
        """
        game = kwargs['game']
        direction = kwargs['qualifier']
        actor = kwargs['actor']
        room = game.rooms[self.container]
        direction = room.directions[direction]
        new_room_key = direction["room"]
        direction_desc = direction["desc"]
        actor.container = new_room_key
        if self.key == "I":
            game.change_game_state("current room", new_room_key)
            game.refresh_things()
            return direction_desc
        else:
            return f"{self.display_name} is in the {game.rooms[new_room_key].display_name}."



