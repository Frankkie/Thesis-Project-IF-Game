

class Display:
    def __init__(self, game):
        self.game = game
        self.text = None
        self._output_queue = []
        self.letter_default_color = 'dddddd'
        self.prompt_color = '33ff33'
        self.help_color = 'ffcc00'
        self.error_color = "ffb000"
        self.dialog_color = '00ff66'

    def queue(self, text, text_type):
        self._output_queue.append((text, text_type))

    def empty_queue(self):
        self._output_queue = []

    def output(self):
        self.print_on_screen()

        for element in self._output_queue:
            self.display(element[0], element[1])
        self.empty_queue()

    def display(self, text, text_type):

        try:
            self.text = text.replace('\n\n\n', '\n')
            self.text = self.text.replace('\n\n', '\n')
        except (TypeError, AttributeError):
            self.text = text

        if text_type == "Error":
            self.__display_error(text)
        elif text_type == "Initial":
            self.__display_init()
        elif text_type == "Prompt":
            self.__display_prompt()
        elif text_type == "AfterAction":
            self.__display_action(text)
        elif text_type == "Dialog":
            self.__display_dialog(text)
        elif text_type == "ChapterStart":
            self.__display_chapter_event()
        elif text_type == "ChapterEvent":
            self.__display_chapter_event()
        elif text_type == "Quit":
            self.__display_quit()
        elif text_type == "Help":
            self.__display_help()
        elif text_type == "Undo":
            self.__display_undo()
        elif text_type == "Save":
            self.__display_save()
        elif text_type == "Replay":
            self.__display_replay()
        elif text_type == 'Specify':
            self.__display_specify()

    def fetch(self):
        command = None
        while not command:
            command = self.game.app.game_screen.current_command
        self.game.app.game_screen.current_command = None
        self.print_on_screen()
        return command

    def __display_prompt(self):
        self.print_on_screen()
        self.print_on_screen(self.text, end="> ", color=self.prompt_color)

    def __display_error(self, error):
        self.print_on_screen()
        self.print_on_screen(error.rstrip(), color=self.error_color)
        self.print_on_screen()

    def __display_action(self, text):
        self.print_on_screen()
        self.print_on_screen(text.rstrip(), color=self.letter_default_color)
        self.print_on_screen()

    def __display_dialog(self, text):
        self.print_on_screen()
        if type(text) == str:
            self.print_on_screen(text, color=self.dialog_color)
        else:
            self.print_on_screen(text[0], color=self.dialog_color)
            try:
                for r in text[1]:
                    self.print_on_screen()
                    self.print_on_screen(r.rstrip(), color=self.dialog_color)
            except IndexError:
                pass
        self.print_on_screen()

    def __display_chapter_event(self):
        self.print_on_screen()
        if type(self.text) == list:
            for result in self.text:
                self.print_on_screen()
                self.print_on_screen(result, color=self.letter_default_color)

        else:
            self.print_on_screen(self.text, color=self.letter_default_color)
        self.print_on_screen()

    def __display_init(self):
        self.print_on_screen(self.game.title, color=self.help_color)
        self.print_on_screen(self.game.credits, color=self.help_color)
        self.print_on_screen('\n\n')

    def __display_help(self):
        self.print_on_screen()
        self.print_on_screen(self.text, color=self.help_color)

    def __display_undo(self):
        self.print_on_screen()
        self.print_on_screen("Your mistake has been forgiven!", color=self.help_color)

    def __display_save(self):
        self.print_on_screen()
        self.print_on_screen("Game saved!", color=self.help_color)

    def __display_quit(self):
        self.print_on_screen()
        self.print_on_screen("You quit '%s'! Such a shame." % self.game.title, color=self.help_color)

    def __display_replay(self):
        self.print_on_screen()
        self.print_on_screen("> " + self.text, color=self.prompt_color)

    def __display_specify(self):
        self.print_on_screen()
        self.print_on_screen(self.text, color=self.help_color)

    def print_on_screen(self, text='\n', **kwargs):
        if 'end' in kwargs.keys():
            text += kwargs['end']
        if 'color' in kwargs.keys():
            text = f'[color={kwargs["color"]}]{text}[/color]'
        self.game.app.game_screen.history.update_game_history(text)
