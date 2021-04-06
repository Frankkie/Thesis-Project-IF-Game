from custom_json import *


if __name__ == "__main__":

    # ROOMS
    ins_room = Room("Small Room", "SmallRoom", "Small Room",
                    description="This is the small room, inside the new room.")

    north_room = Room("North Room", "NorthRoom", "North Room",
                      description="This is the North Room, north of the New Room.")

    new_room = Room("New Room", "NewRoom", "New Room", description="This is a new room.")

    new_room += [ins_room, "There is a small room."]
    new_room &= ["North", north_room, "To the north there is the North Room."]

    custom_dump({"New Room": new_room}, "rooms.json")
    rooms = custom_load("rooms.json")
    print(rooms["New Room"].directions["North"][0].string())

    # Verbs
    """Verbs = custom_load("verbs.json")
    custom_dump(Verbs, "verbs.json")
    print(Verbs)"""