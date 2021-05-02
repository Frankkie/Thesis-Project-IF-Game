from entities import Entity
import json


class Actor(Entity):
    """
    This is the parent class of all Actors.
    """
    def __init__(self, *args, abilities=None, on_command=None, **kwargs):
        """
        The constructor of actors.
        :param args: arguments passed to the Entity constructor
        :param abilities: dict, keys: verb names, values: boolean, depending on whether or not this actor
                          can perform this action.
        :param on_command: dict, keys: verb names, values: boolean, depending on whether or not this actor
                          can be currently commanded to perform this action.
        :param kwargs: keyword arguments passed to the Entity constructor
        """
        super().__init__(*args, **kwargs)

        with open("Grammar/verbs.json", "r") as file:
            verbs = json.load(file)  # Load dict of all verbs
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
        The method triggered when the Go Verb is given by the player to the actor.
        :param kwargs:
        :return:
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



