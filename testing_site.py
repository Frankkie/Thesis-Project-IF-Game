import game
import custom_json as cjson


if __name__ == "__main__":
    actors = cjson.custom_load("Games/Test/actors.json")
    verbs = cjson.custom_load("Grammar/verbs.json")
    rooms = cjson.custom_load("Games/Test/rooms.json")

    game_state = {"current room": "New Room"}
    game_ = game.Game("Test Game", "by Christos Frantzolas", game_state)
    game_.boot_game(actors, verbs, rooms)
