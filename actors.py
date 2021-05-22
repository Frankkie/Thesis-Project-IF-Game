"""
The module of the Actor class and its subclasses.

Classes:
    Actor(Entity)

"""

from entities import Entity
from errors import ActionError
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
    def __init__(self, *args, gender, active_convonode='ready', is_known=True,
                 abilities=None, on_command=None, **kwargs):
        """
        The constructor of actors.
        :param args:
            arguments passed to the Entity constructor
        :param gender: int, can be 0, 1, 2, 3
            the gender of the actor. 0 is she/her, 1 is he/him, 2 is they/them, 3 is it/it.
        :param active_convonode: str, default: 'ready'
            the key of the convonode active for this actor.
        :param is_known: bool, default: True
            True if the Actor can be interacted with by the player.
        :param abilities: dict
            keys: verb names, values: boolean, depending on whether or not this actor can perform this action.
        :param on_command: dict
            keys: verb names, values: boolean, depending on whether or not this actor can be currently commanded
            to perform this action.
        :param kwargs:
            keyword arguments passed to the Entity constructor
        """
        super().__init__(*args, **kwargs)

        self.gender = gender
        self.active_convonode = active_convonode
        self.is_known = is_known

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
        direction_key = kwargs['qualifier']
        actor = kwargs['actor']
        room = game.rooms[self.container]
        direction = room.directions[direction_key]
        new_room_key = direction["room"]

        if room.__class__.__name__ == "Door":
            if room.entity_state['Open'] is False and room.active_direction != direction_key:
                raise ActionError('DoorClosedError', direction=direction_key, door=room.display_name)

        new_room = game.rooms[new_room_key]
        direction_desc = f'{new_room.display_name.capitalize()}:\n{new_room.description}'
        actor.container = new_room_key
        if self.key == "I":
            game.change_game_state("current room", new_room_key)
            game.refresh_things()
            return direction_desc
        else:
            return f"{self.display_name} is in the {game.rooms[new_room_key].display_name}."

    def _on_takeoff(self, **kwargs):
        """
        Triggered by the Takeoff verb.
        Changes the actor's room depending on the qualifier (direction) given.

        :param kwargs:
            Keyword args should include 'game', 'qualifier' and 'actor'
        :return: str

        """
        game = kwargs['game']
        planet_key = game.game_state['current planet']
        planet = game.things[planet_key]
        return planet.on_take_off(game=game)




