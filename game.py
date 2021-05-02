"""
    This is the file for the Game class, the class that holds all the important information
    about the game and its state.
"""
import sys
import my_parser as prs
from command_handler import CommandHandler
from display import Display
from errors import *


class Game:
    def __init__(self, title, credits_, game_state=None, seed=0):
        self.title = title
        self.credits = credits_
        self.game_state = game_state
        self.seed = seed
        self.display = None
        self.command_handler = CommandHandler(self)
        self.parser = prs.Parser(self)
        self.preparser = prs.PreParser()
        self.actors = {}
        self.verbs = {}
        self.things = {}
        self.rooms = {}

    def boot_game(self, actors, verbs, rooms, display):
        self.verbs = verbs
        self.rooms = rooms
        self.actors = actors
        self.display = display
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
        # Print starting description
        self.game_state["new game"] = False
        while True:
            self.run_pc_turn()

    def run_pc_turn(self):
        # Get user's command.
        pc_command = self.get_command("")
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

    def change_game_state(self, key, value):
        if key in self.game_state.keys():
            self.game_state[key] = value
        else:
            raise ValueError

    def quit_game(self):
        self.display.display("", "Quit")
        sys.exit(0)

    def save_game(self, display=True):
        if display:
            self.display.display("", "Save")
        return

    def load_chapter(self, chapter_key):
        return

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



