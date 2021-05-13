

class Display:
    def __init__(self, game):
        self.game = game
        self.text = None
        self.output_queue = []

    def queue(self, text, text_type):
        self.output_queue.append((text, text_type))

    def empty_queue(self):
        self.output_queue = []

    def output(self):
        for element in self.output_queue:
            self.display(element[0], element[1])
        self.empty_queue()

    def display(self, text, text_type):
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

    def fetch(self):
        text = input()
        return text

    def __display_prompt(self):
        print(self.text, end="> ")

    def __display_error(self, error):
        print(error)
        print("\n")

    def __display_action(self, text):
        print(text)
        print()

    def __display_dialog(self, text):
        print(text[0])
        try:
            for r in text[1]:
                print(r)
            print()
        except IndexError:
            pass

    def __display_chapter_event(self):
        if type(self.text) == list:
            for result in self.text:
                print(result)
            print()
        else:
            print(self.text)
            print()

    def __display_init(self):
        print(self.game.title)
        print(self.game.credits)
        print("\n")

    def __display_help(self):
        print(self.text)
        print("\n")

    def __display_undo(self):
        print("Your mistake has been forgiven!")
        print("\n")

    def __display_save(self):
        print("Game saved!")
        print("\n")

    def __display_quit(self):
        print("You quit '%s'! Such a shame." % self.game.title)
        print("\n")

    def __display_replay(self):
        print("> " + self.text)
