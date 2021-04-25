"""
    This is the file for the Game class, the class that holds all the important information
    about the game and its state.
"""
import sys
import my_parser as prs


def error_message(error_type):
    """
    This function prints an error message.
    :param error_type: A string.
    :return: None
    """
    if error_type == "GrammarError":
        return "I could not understand your command."
    if error_type == "VerbError":
        return "I could not understand this verb."
    if error_type == "SyntaxError":
        return "This is the incorrect syntax for this verb."
    if error_type == "EntityError":
        return "This object is not here."


class Display:
    def __init__(self, game):
        self.game = game
        self.text = None

    def display(self, text, text_type):
        self.text = text
        if text_type == "Error":
            self.__display_error()
        elif text_type == "Initial":
            self.__display_init()
        elif text_type == "Prompt":
            self.__display_prompt()
        elif text_type == "AfterAction":
            self.__display_action()
        elif text_type == "Quit":
            self.__display_quit()
        elif text_type == "Help":
            self.__display_help()
        elif text_type == "Undo":
            self.__display_undo()
        elif text_type == "Save":
            self.__display_save()

    def fetch(self):
        text = input()
        return text

    def __display_prompt(self):
        print(self.text, end="> ")

    def __display_error(self):
        print(error_message(self.text))

    def __display_action(self):
        print(self.text)

    def __display_init(self):
        print(self.game.title)
        print(self.game.credits)

    def __display_help(self):
        print("No one can help you!")

    def __display_undo(self):
        print("Mistakes are forever!")

    def __display_save(self):
        print("No one can save you!")

    def __display_quit(self):
        print("You quit '%s'! Such a shame." % self.game.title)


class CommandHandler:
    def __init__(self, game):
        self.command = None
        self.syntax = ""
        self.game = game

    def run_command(self, sentence, syntax):
        self.command = sentence
        self.syntax = syntax

        # If this command is directed to the Player Character
        if sentence["Actor"] == self.game.actors["I"]:
            result = self.pc_command(sentence, syntax)
        # If this command is directed to an NPC
        else:
            result = self.npc_command(sentence, syntax)
        return result

    def pc_command(self, sentence, syntax):
        # Prepare for action
        prep = self.prepare_execution(sentence, syntax)
        if prep and type(prep) != str:
            # Execute action
            res = self.action_execution(sentence, syntax)
            return res
        else:
            return prep

    def npc_command(self, sentence, syntax):
        # Check npc commandability
        # Prepare for action
        prep = self.prepare_execution(sentence, syntax)
        if prep and type(prep) != str:
            # Execute action
            res = self.action_execution(sentence, syntax)
            return res
        else:
            return prep

    def prepare_execution(self, sentence, syntax):
        """
        This method determines whether the command given by the player can be executed.
        If the action is allowed, the method returns True.
        If not, the method returns an error code (string).
        :param sentence: Dictionary with the command parts.
        :param syntax: The syntax of the command.
        :return: True if the action is allowed, an error code (str) if the action is not allowed.
        """
        return True

    def action_execution(self, sentence, syntax):
        return sentence, syntax

    def __check_actor(self):
        return True

    def __check_qualifier(self):
        return True

    def __check_object(self):
        return True

    def __check_ind_object(self):
        return True

    def __check_preconditions(self):
        return True

    def __save_game_state(self):
        return

    def __action_(self, sentence):
        return sentence

    def __action_q(self, sentence):
        return sentence

    def __action_o(self, sentence):
        return sentence

    def __action_oqi(self, sentence):
        return sentence


class Game:
    def __init__(self, title, credits_, curr_room):
        self.title = title
        self.credits = credits_
        self.current_room = curr_room
        self.display = Display(self)
        self.command_handler = CommandHandler(self)
        self.parser = prs.Parser(self)
        self.preparser = prs.PreParser()
        self.actors = {}
        self.verbs = {}
        self.things = {}
        self.rooms = {}

    def boot_game(self, actors, things, verbs):
        self.actors = actors
        self.things = things
        self.verbs = verbs
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
        # If this is any other command type.
        else:
            self.display.display("", cmd_type)

    def parsable_command(self, command):
        parts = self.parser.run_parser(command)
        # In case of Error.
        if type(parts) == str:
            return parts
        # DISAMBIGUATE COMMANDS BEFORE THIS POINT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        result = []
        # For all the commands.
        for sentence in parts:
            sentence = sentence[0]
            syntax = self.id_syntax_pattern(sentence)
            # If this command is directed to the Player Character
            res = self.command_handler.run_command(sentence, syntax)
            if type(res) == str:
                return res
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

    def quit_game(self):
        self.display.display("", "Quit")
        sys.exit(0)



