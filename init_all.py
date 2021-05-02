from game import Game
from display import Display
import json
import custom_json as cjson


class Initializer:
    """
    The class that handles the program before a game is launched.
    """

    def __init__(self):
        self.display = Display(None)
        self.game = None
        self.info = {
            "display": self.display,
            "actors": None,
            "verbs": None,
            "rooms": None
        }

    def load_game(self):
        game_name = "Test"
        folder = "Games/" + game_name
        file = folder + "/game.json"
        self.__load_game(file)
        self.display.game = self.game
        self.__load_info(folder)
        self.game.boot_game(**self.info)

    def __load_game(self, path):
        with open(path, "r") as file:
            dct = json.load(file)
        self.game = Game(**dct)

    def __load_info(self, path):
        # CHANGE THIS WHEN YOU ADD SCENES
        actors_file = path + "/actors.json"
        chapter_folder = path + "/" + self.game.game_state["current chapter"]
        room_file = path + "/rooms.json"
        verb_file = "Grammar/verbs.json"

        self.info["actors"] = cjson.custom_load(actors_file)
        self.info["verbs"] = cjson.custom_load(verb_file)
        self.info["rooms"] = cjson.custom_load(room_file)


if __name__ == "__main__":
    init = Initializer()
    init.load_game()




