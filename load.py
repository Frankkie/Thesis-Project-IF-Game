"""
Load games.

Classes:
    Loader

"""


import os
import json

from tools import empty_folder, copytree
import custom_json as cjson


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
        log_file_path = f"Games\\{title}\\log_commands.log"
        commands = []
        with open(log_file_path, "r") as log_file:
            for line in log_file:
                commands.append(line.rstrip())
        return commands

    def load_chapter(self, chapter_key, start=False):
        # Save to current folder before the Chapter Change, so that
        # the changes to the rooms are saved.
        if not start:
            self.game.saver.save_to_current()

        chapter = self.game.chapters[chapter_key]

        try:
            convonodes_file = os.path.join(self.current_folder, "convoNodes", chapter.convonodes_file)
        except TypeError:
            convonodes_file = None
        try:
            dialogevents_file = os.path.join(self.current_folder, "dialogEvents", chapter.dialogevents_file)
        except TypeError:
            dialogevents_file = None
        try:
            events_file = os.path.join(self.current_folder, "events", chapter.events_file)
        except TypeError:
            events_file = None
        maps_file = os.path.join(self.current_folder, "maps", chapter.map_file)
        try:
            topics_file = os.path.join(self.current_folder, "topics", chapter.topics_file)
        except TypeError:
            topics_file = None

        self.game.rooms = cjson.custom_load(maps_file)
        if convonodes_file:
            self.game.convonodes = cjson.custom_load(convonodes_file)
        if dialogevents_file:
            self.game.dialogevents = cjson.custom_load(dialogevents_file)
        if events_file:
            self.game.events = cjson.custom_load(events_file)
        if topics_file:
            self.game.topics = cjson.custom_load(topics_file)

        self.game.game_state["current chapter"] = chapter_key

        if chapter.first_room:
            self.game.game_state["current room"] = chapter.first_room
            for actor in self.game.actors.values():
                actor.container = chapter.first_room

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


