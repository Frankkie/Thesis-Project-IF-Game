from custom_json import custom_load
from custom_json import custom_dump
import my_parser
import os
from things import *


if __name__ == "__main__":
    """things = {}
    things["green tomato"] = Thing("green tomato", "tomato", "the green tomato",
                                   reference_adjectives=["green", "plump"])
    things["yellow dog"] = Thing("yellow dog", "dog", "the yellow dog",
                                 reference_adjectives=["yellow", "big"])
    things["golden duck"] = Thing("golden duck", "duck", "the golden duck",
                                  reference_adjectives=["gold", "golden"])

    custom_dump(things, "test_things.json")"""
    while True:
        text = input("> ")
        parser = my_parser.Parser(custom_load("actors.json"), custom_load("verbs.json"),
                                  custom_load("test_things.json"))
        parts = parser.run_parser(text)
        print(parts)

        if text == "quit":
            break

    # ROOMS
    """ins_room = Room("Small Room", "SmallRoom", "Small Room",
                    description="This is the small room, inside the new room.")

    north_room = Room("North Room", "NorthRoom", "North Room",
                      description="This is the North Room, north of the New Room.")

    new_room = Room("New Room", "NewRoom", "New Room", description="This is a new room.")

    new_room += [ins_room, "There is a small room."]
    new_room &= ["North", north_room, "To the north there is the North Room."]

    custom_dump({"New Room": new_room}, "rooms.json")
    rooms = custom_load("rooms.json")
    print(rooms["New Room"].directions["North"][0].string())"""

    # Verbs
    """Verbs = custom_load("verbs.json")
    custom_dump(Verbs, "verbs.json")
    print(Verbs)"""