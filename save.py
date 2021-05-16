"""
Save games.

Classes:
    Saver

"""


import os
import json

import custom_json as cjson
from tools import empty_folder, copytree
import time
import shutil


class Saver:
    """

    """
    def __init__(self, game):
        """

        """
        self.game = game
        self.title = game.title
        self.game_folder = game.loader.game_folder
        self.current_folder = game.loader.current_folder

    def save_to_current(self):
        chapter_key = self.game.game_state["current chapter"]
        chapter = self.game.chapters[chapter_key]

        for file in chapter.convonodes_files:
            f = os.path.join(self.current_folder, "convoNodes", (file + ".json"))
            file = file.split('.')
            cjson.custom_dump(self.game.convonodes[file[0]][file[1]], f)

        for file in chapter.dialogevents_files:
            f = os.path.join(self.current_folder, "dialogEvents", (file + ".json"))
            cjson.custom_dump(self.game.dialogevents[file], f)

        for file in chapter.events_files:
            f = os.path.join(self.current_folder, "events", (file + ".json"))
            cjson.custom_dump(self.game.events[file], f)

        for file in chapter.topics_files:
            f = os.path.join(self.current_folder, "topics", (file + ".json"))
            cjson.custom_dump(self.game.topics[file], f)

        for file in chapter.map_files:
            f = os.path.join(self.current_folder, "maps", (file + ".json"))
            cjson.custom_dump(self.game.rooms[file], f)

        # Save Actors
        cjson.custom_dump(self.game.actors, os.path.join(self.current_folder, "actors.json"))
        # Save Chapters
        cjson.custom_dump(self.game.chapters, os.path.join(self.current_folder, "chapters.json"))

        # Save Game
        with open(os.path.join(self.current_folder, "game.json"), "w") as file:
            json.dump(self.game.to_json(), file)
        file.close()

    def save_to_temp(self):
        temp_folder = os.path.join(self.game_folder + "_temp", "")
        empty_folder(temp_folder)
        copytree(self.current_folder, temp_folder)
        return

    def save_game(self, display=True, quit_=False):
        current_time = int(time.time())
        save_folder = os.path.join(self.game_folder, f"save_{current_time}", "")

        for root, subdirs, files in os.walk(self.game_folder):
            for d in subdirs:
                if "save_" in d:
                    shutil.rmtree(os.path.join(root, d))

        with open(os.path.join(self.game_folder, "load_game.json"), "r") as load_file:
            load_info = json.load(load_file)
        load_file.close()
        load_info["last_save_key"] = f"save_{current_time}"
        with open(os.path.join(self.game_folder, "load_game.json"), "w") as load_file:
            json.dump(load_info, load_file)
        load_file.close()

        self.save_to_current()
        os.mkdir(save_folder)
        copytree(self.current_folder, save_folder)
        if display:
            self.game.display.queue("", "Save")

        if quit_:
            self.empty_current_temp()
        return

    def empty_current_temp(self):
        empty_folder(self.current_folder)
        temp_folder = os.path.join(self.game_folder + "_temp", "")
        empty_folder(temp_folder)





