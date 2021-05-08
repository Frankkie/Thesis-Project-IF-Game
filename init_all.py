import json

import custom_json as cjson
from display import Display
from game import Game
from tools import copytree, empty_folder


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
            "chapters": None
        }

    def load_game(self):
        game_name = "Test"
        save_folder = self.__find_save_folder(game_name)
        empty_folder("Games\\" + game_name + "\\current")
        copytree(save_folder, "Games\\" + game_name + "\\current")

        save_folder = "Games\\" + game_name + "\\current"

        self.__load_game(save_folder)
        self.display.game = self.game

        self.__load_info(save_folder)

        self.game.boot_game(**self.info)

    def __find_save_folder(self, game_name):
        folder = "Games\\" + game_name
        with open(folder + "\\load_game.json", "r") as load_file:
            load_info = json.load(load_file)
        load_file.close()
        self.info = {**self.info, **load_info}
        if self.info["last_save_key"]:
            save_folder = folder + "\\" + self.info["last_save_key"]
        else:
            save_folder = folder + "\\_read_only"
        return save_folder

    def __load_game(self, path):
        path += "\\game.json"
        with open(path, "r") as file:
            dct = json.load(file)
        file.close()
        self.game = Game(**dct)

    def __load_info(self, path):
        actors_file = path + "\\actors.json"
        chapters_file = path + "\\chapters.json"
        verb_file = "Grammar\\verbs.json"

        self.info["actors"] = cjson.custom_load(actors_file)
        self.info["verbs"] = cjson.custom_load(verb_file)
        self.info["chapters"] = cjson.custom_load(chapters_file)


if __name__ == "__main__":
    init = Initializer()
    init.load_game()




