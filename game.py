"""
    This is the file for the Game class, the class that holds all the important information
    about the game and its state.
"""


import os
import sys
import time
import shutil

import custom_json as cjson
import my_parser as prs
from command_handler import CommandHandler
from errors import *
from tools import empty_folder, copytree
from log_commands import start_log, log_command


class Game:
    def __init__(self, title, credits_, game_state=None, seed=0, last_save_key=None):
        self.title = title
        self.credits = credits_
        self.game_state = game_state
        self.seed = seed
        self.last_save_key = last_save_key
        self.display = None
        self.command_handler = CommandHandler(self)
        self.parser = prs.Parser(self)
        self.preparser = prs.PreParser()
        self.actors = {}
        self.verbs = {}
        self.rooms = {}
        self.chapters = {}
        self.topics = {}  # HAVE LOAD TOPICS AS WELL
        start_log(self)

    def boot_game(self, actors, verbs, chapters, display, last_save_key):
        self.verbs = verbs
        self.chapters = chapters
        self.actors = actors
        self.display = display
        self.last_save_key = last_save_key
        self.load_chapter(self.game_state["current chapter"], start=True)
        self.refresh_things()
        self.display.display("", "Initial")
        # Print boot up description
        # begin = self.get_command("Do you want to begin? (y/n) ")
        begin = "y"
        if begin == "y":
            self.start_game()
        else:
            self.quit_game()

    def start_game(self):
        self.game_state["new game"] = False
        self.run_chapter(start=True)
        while True:
            self.save_to_temp()
            self.run_pc_turn()
            self.run_chapter()
            self.save_to_current()
            self.game_state["turn count"] += 1

    def run_pc_turn(self):
        # Get user's command.
        pc_command = self.get_command("")
        command_text = pc_command
        # Preparse command.
        self.preparser.run_preparser(pc_command)
        pc_command = self.preparser.text
        cmd_type = self.preparser.cmd_type

        # If this is a parsable command
        if cmd_type == "Command":
            result = self.parsable_command(pc_command)
            if type(result) == str:
                self.display.display(result, "Error")
            else:
                self.display.display(result, "AfterAction")

        # If this is a quit command
        elif cmd_type == "Quit":
            self.quit_game()
            return
        elif cmd_type == "Save":
            self.save_game()
        # If this is any other command type.
        else:
            self.display.display("", cmd_type)

        log_command(self, command_text)

    def parsable_command(self, command):
        try:
            parts = self.parser.run_parser(command)
        # In case of Error.
        except ParserError as error:
            return str(error)
        # DISAMBIGUATE COMMANDS BEFORE THIS POINT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        result = []
        # For all the commands.
        for sentence in parts:
            sentence = sentence[0]
            syntax = self.id_syntax_pattern(sentence)
            # If this command is directed to the Player Character
            try:
                res = self.command_handler.run_command(sentence, syntax)
            except (CheckCommandError, PreconditionsError, ActionError) as error:
                return str(error)
            result.append(res)
        return result

    def id_syntax_pattern(self, tree):
        pattern = ""
        if tree["Object"]:
            pattern += "O"
        if tree["Qualifier"]:
            pattern += "Q"
        if tree["Indirect"]:
            pattern += "I"
        return pattern

    def get_command(self, text):
        self.display.display(text, "Prompt")
        command = self.display.fetch()
        return command

    def load_chapter(self, chapter_key, start=False):
        current_folder = "Games\\" + self.title + "\\current"
        chapter_folder = current_folder + "\\_chapter_" + chapter_key
        events_file_path = chapter_folder + "\\events.json"

        # Save to current folder before the Chapter Change, so that
        # the changes to the rooms are saved.
        if not start:
            self.save_to_current()

        self.game_state["current chapter"] = chapter_key
        chapter = self.chapters[chapter_key]
        if chapter.first_room:
            self.game_state["current room"] = chapter.first_room
            for actor in self.actors.values():
                actor.container = chapter.first_room

        rooms_file_name = chapter.room_file
        rooms_file_path = current_folder + "\\_rooms_\\" + rooms_file_name
        self.rooms = cjson.custom_load(rooms_file_path)
        try:
            events = cjson.custom_load(events_file_path)
            self.chapters[chapter_key].events = events
        except FileNotFoundError:
            pass

    def run_chapter(self, start=False):
        active_chapter_key = self.game_state["current chapter"]
        active_chapter = self.chapters[active_chapter_key]
        if start:
            result = active_chapter.start_chapter()
            self.display.display(result, "ChapterStart")
            if result["Next Chapter"]:
                next_chapter = result["Next Chapter"]
                if next_chapter == "__END__":
                    self.end_game()

        else:
            result = active_chapter.advance_chapter(self)
            self.display.display(result, "ChapterEvent")
            if result["Next Chapter"]:
                next_chapter = result["Next Chapter"]
                self.load_chapter(next_chapter)
                self.refresh_things()
                self.run_chapter(start=True)

    def change_game_state(self, key, value):
        if key in self.game_state.keys():
            self.game_state[key] = value
        else:
            raise ValueError

    def quit_game(self):
        self.display.display("", "Quit")
        self.end_game()

    def end_game(self):
        self.display.display("Do you want to save this game? (y/n)", "Prompt")
        reply = self.display.fetch()
        if reply in ["y", "yes", "Y", "Yes", "YES"]:
            self.save_game()
        elif reply in ["n", "N", "No", "NO", "no"]:
            pass
        else:
            self.end_game()
        sys.exit(0)

    def refresh_things(self):
        new_things = {}
        current_room_key = self.game_state["current room"]
        current_room = self.rooms[current_room_key]
        for actor in self.actors.keys():
            if self.actors[actor].container == current_room_key:
                new_things = {**new_things, **self.actors[actor].get_contents()}
                new_things[actor] = self.actors[actor]
        new_things = {**new_things, **current_room.get_contents()}
        self.things = new_things

    def save_to_current(self):
        chapter_key = self.game_state["current chapter"]
        chapter = self.chapters[chapter_key]
        room_file_name = chapter.room_file
        current_folder = f"Games\\{self.title}\\current"
        chapter_folder = current_folder + "\\_chapter_" + chapter_key
        rooms_folder = current_folder + "\\_rooms_\\"
        # Save Actors
        cjson.custom_dump(self.actors, current_folder+"\\actors.json")
        # Save Chapters
        cjson.custom_dump(self.chapters, current_folder+"\\chapters.json")
        # Save Game
        cjson.custom_dump(self.chapters, current_folder+"\\game.json")
        # Save Rooms
        cjson.custom_dump(self.rooms, rooms_folder+room_file_name)
        # Save Events
        if chapter.events:
            cjson.custom_dump(chapter.events, chapter_folder+"\\events.json")

    def save_to_temp(self):
        temp_folder = "Games\\" + self.title + "\\_temp"
        current_folder = "Games\\" + self.title + "\\current"
        empty_folder(temp_folder)
        copytree(current_folder, temp_folder)
        return

    def save_game(self, display=True):
        current_time = int(time.time())
        save_folder = f"Games\\{self.title}\\save_{current_time}"
        current_folder = f"Games\\{self.title}\\current"
        for root, subdirs, files in os.walk('Games\\'+self.title):
            for d in subdirs:
                if "save_" in d:
                    shutil.rmtree(os.path.join(root, d))
        self.save_to_current()
        os.mkdir(save_folder)
        copytree(current_folder, save_folder)
        if display:
            self.display.display("", "Save")
        return



