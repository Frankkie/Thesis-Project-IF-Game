"""
    This is the file for the Game class, the class that holds all the important information
    about the game and its state.
"""


import sys

import my_parser as prs
from command_handler import CommandHandler
from errors import *
from log_commands import start_log, log_command
from load import Loader
from save import Saver


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
        self.np_parser = prs.NounPhraseParser(self)
        self.loader = Loader(self.title, self)
        self.saver = Saver(self)
        self.actors = {}
        self.verbs = {}
        self.rooms = {}
        self.chapters = {}
        self.things = {}
        self.topics = {}
        self.convonodes = {}
        self.dialogevents = {}
        self.events = {}

    def boot_game(self, actors, verbs, chapters, display, last_save_key, replay=False):
        self.actors = actors
        self.verbs = verbs
        self.chapters = chapters
        self.display = display
        self.last_save_key = last_save_key
        self.loader.load_chapter(self.game_state["current chapter"], start=True)
        self.refresh_things()

        if replay:
            self.replay_game()

        start_log(self)
        self.display.queue("", "Initial")
        self.display.output()
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
            self.saver.save_to_temp()
            self.run_pc_turn()
            self.display.output()
            self.run_chapter()
            self.display.output()
            self.saver.save_to_current()
            self.game_state["turn count"] += 1

    def replay_game(self):
        commands = self.loader.load_prev_commands(self.title)
        self.game_state["new game"] = False
        self.run_chapter(start=True)
        for command in commands:
            self.saver.save_to_temp()
            self.run_pc_turn(command)
            self.display.output()
            self.run_chapter()
            self.display.output()
            self.saver.save_to_current()
            self.game_state["turn count"] += 1

        while True:
            self.saver.save_to_temp()
            self.run_pc_turn()
            self.display.output()
            self.run_chapter()
            self.display.output()
            self.saver.save_to_current()
            self.game_state["turn count"] += 1

    def run_pc_turn(self, command=None):
        # Get user's command.
        if not command:
            pc_command = self.get_command("")
            log_command(self, pc_command)
        else:
            pc_command = command
            self.display.queue(command, "Replay")
            self.display.output()

        # Preparse command.
        self.preparser.run_preparser(pc_command)
        pc_command = self.preparser.text
        cmd_type = self.preparser.cmd_type

        # If this is a parsable command
        if cmd_type == "Command":
            self.parsable_command(pc_command)
            # self.display.display(result, "AfterAction")

        # If this is a quit command
        elif cmd_type == "Quit":
            self.quit_game()
            return
        elif cmd_type == "Save":
            self.saver.save_game()
        # If this is any other command type.
        else:
            self.display.queue("", cmd_type)

    def parsable_command(self, command):
        try:
            parts = self.parser.run_parser(command)
        # In case of Error.
        except ParserError as error:
            self.display.queue(str(error), "Error")
            return

        try:
            parts = self.np_parser.run_np_parser(parts)
        except (ParserError, NPParserError, DialogError) as error:
            self.display.queue(str(error), "Error")
            return

        # DISAMBIGUATE COMMANDS BEFORE THIS POINT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # For all the commands.
        for sentence in parts:
            sentence = sentence[0]
            syntax = self.id_syntax_pattern(sentence)
            # If this command is directed to the Player Character
            try:
                self.command_handler.run_command(sentence, syntax)
            except (CheckCommandError, PreconditionsError, ActionError, DialogError) as error:
                self.display.queue(str(error), "Error")
                return

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
        self.display.queue(text, "Prompt")
        self.display.output()
        command = self.display.fetch()
        return command

    def run_chapter(self, start=False):
        active_chapter_key = self.game_state["current chapter"]
        active_chapter = self.chapters[active_chapter_key]
        if start:
            next_chapter = active_chapter.start_chapter(self)
            if next_chapter:
                if next_chapter == "__END__":
                    self.end_game()

        else:
            next_chapter = active_chapter.advance_chapter(self)

            if next_chapter:
                self.loader.load_chapter(next_chapter)
                self.refresh_things()
                self.run_chapter(start=True)

    def change_game_state(self, key, value):
        if key in self.game_state.keys():
            self.game_state[key] = value
        else:
            raise ValueError

    def quit_game(self):
        self.display.queue("", "Quit")
        self.display.output()
        self.end_game()

    def end_game(self):
        self.display.queue("Do you want to save this game? (y/n)", "Prompt")
        self.display.output()
        reply = self.display.fetch()
        if reply in ["y", "yes", "Y", "Yes", "YES"]:
            self.saver.save_game(quit_=True)
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

    def to_json(self):
        """
        Convert the instance of this class to a serializable object.

        :return: Dictionary
            A dictionary of the object's attributes, containing the key '_class_'.

        """
        obj_dict = {
            "title": self.title,
            "credits_": self.credits,
            "game_state": self.game_state,
            "last_save_key": self.last_save_key,
            "seed": self.seed
        }
        return obj_dict

