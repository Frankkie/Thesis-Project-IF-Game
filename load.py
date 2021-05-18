"""
Load games.

Classes:
    Loader

"""


import os
import json

from tools import empty_folder, copytree
import custom_json as cjson
from errors import CheckCommandError


class Loader:
    """

    """
    def __init__(self, game_name, game, from_save=False):
        # The game object.
        self.game = game
        # The directory of all game saves.
        self.game_folder = None
        # The Games/{game_name}/current_folder
        self.current_folder = None
        # The folder in which the last save of the game exists.
        self.save_folder = None
        # The arguments going into the game constructor.
        self.game_args = {
            "actors": None,
            "display": None,
            "verbs": None,
            "chapters": None
        }
        self.__find_save_folder(game_name, from_save)

    def load_game(self, display):
        self.game_args["display"] = display
        empty_folder(self.current_folder)
        copytree(self.save_folder, self.current_folder)
        game_dict = self.__load_game_file(self.current_folder)
        self.__load_game_files(self.current_folder)
        return game_dict, self.game_args

    def load_prev_commands(self, title):
        log_file_path = os.path.join('Games', title, "log_commands.log")
        commands = []
        times = []
        with open(log_file_path, "r") as log_file:
            for line in log_file:
                try:
                    time = float(line.rstrip())
                    times.append(time)
                except ValueError:
                    commands.append(line.rstrip())
        return commands, times

    def load_prev_seed(self, title):
        log_file_path = os.path.join('Games', title, "log_seed.log")

        with open(log_file_path, "r") as log_file:
            for line in log_file:
                seed = int(line.rstrip())
        return seed

    def load_undo(self):
        temp_folder = os.path.join(self.game_folder + "_temp", "")
        if not os.listdir(temp_folder):
            raise CheckCommandError('UndoError')
        empty_folder(self.current_folder)
        copytree(temp_folder, self.current_folder)
        empty_folder(temp_folder)
        game_dct = self.__load_game_file(self.current_folder)
        self.game.game_state = game_dct['game_state']
        # Load game parameters, chapters and actors
        actors_file = os.path.join(self.current_folder, "actors.json")
        chapters_file = os.path.join(self.current_folder, "chapters.json")

        self.game.actors = cjson.custom_load(actors_file)
        self.game.chapters = cjson.custom_load(chapters_file)

        # Load Chapter again
        self.load_chapter(self.game.game_state['current chapter'], undo=True)

    def load_chapter(self, chapter_key, start=False, undo=False):
        # Save to current folder before the Chapter Change, so that
        # the changes to the rooms are saved.
        if not start and not undo:
            self.game.saver.save_to_current()

        chapter = self.game.chapters[chapter_key]

        convonodes_files = [os.path.join(self.current_folder, "convoNodes", (file + ".json")) for file in
                            chapter.convonodes_files]
        dialogevents_files = [os.path.join(self.current_folder, "dialogEvents", (file + ".json")) for file in
                              chapter.dialogevents_files]
        events_files = [os.path.join(self.current_folder, "events", (file + ".json")) for file in chapter.events_files]
        map_files = [os.path.join(self.current_folder, "maps", (file + ".json")) for file in chapter.map_files]
        topics_files = [os.path.join(self.current_folder, "topics", (file + ".json")) for file in chapter.topics_files]

        for i, file in enumerate(convonodes_files):
            f = chapter.convonodes_files[i].split('.')
            actor = f[0]
            node = f[1]
            obj = cjson.custom_load(file)
            if actor in self.game.convonodes.keys():
                self.game.convonodes[actor][node] = obj
            else:
                self.game.convonodes[actor] = {}
                self.game.convonodes[actor][node] = obj

        for file in dialogevents_files:
            obj = cjson.custom_load(file)
            self.game.dialogevents[obj.key] = obj

        for file in events_files:
            obj = cjson.custom_load(file)
            self.game.events[obj.key] = obj

        for file in topics_files:
            obj = cjson.custom_load(file)
            self.game.topics[obj.key] = obj

        for file in map_files:
            obj = cjson.custom_load(file)
            self.game.rooms[obj.key] = obj

        self.game.game_state["current chapter"] = chapter_key

        if chapter.first_room and not undo:
            self.game.game_state["current room"] = chapter.first_room
            for actor in self.game.actors.values():
                actor.container = chapter.first_room

        if undo:
            self.game.refresh_things()

    def __find_save_folder(self, game_name, from_save):
        self.game_folder = os.path.join("Games", game_name, "")
        self.current_folder = os.path.join(self.game_folder, "current", "")
        with open(os.path.join(self.game_folder, "load_game.json"), "r") as load_file:
            load_info = json.load(load_file)
        load_file.close()

        self.game_args = {**self.game_args, **load_info}
        if not from_save:
            self.game_args["last_save_key"] = None

        if self.game_args["last_save_key"]:
            self.save_folder = os.path.join(self.game_folder, self.game_args["last_save_key"], "")
        else:
            self.save_folder = os.path.join(self.game_folder, "_read_only", "")

    def __load_game_file(self, path):
        with open(os.path.join(path, "game.json"), "r") as file:
            dct = json.load(file)
        file.close()
        return dct

    def __load_game_files(self, path):
        actors_file = os.path.join(path, "actors.json")
        chapters_file = os.path.join(path, "chapters.json")
        verb_file = os.path.join("Grammar", "verbs.json")

        self.game_args["actors"] = cjson.custom_load(actors_file)
        self.game_args["verbs"] = cjson.custom_load(verb_file)
        self.game_args["chapters"] = cjson.custom_load(chapters_file)


