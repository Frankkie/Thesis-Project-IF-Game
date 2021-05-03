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

    def fetch(self):
        text = input()
        return text

    def __display_prompt(self):
        print(self.text, end="> ")

    def __display_error(self):
        print(self.text)

    def __display_action(self):
        for command in self.text:
            for sentence in command['Descriptions']:
                print(sentence, end=" ")
            print()

    def __display_chapter_event(self):
        if not self.text["Descriptions"]:
            return
        for result in self.text["Descriptions"]:
            print(result, end=" ")
        print()

    def __display_init(self):
        print(self.game.title)
        print(self.game.credits)

    def __display_help(self):
        print("No one can help you!")

    def __display_undo(self):
        print("Mistakes are forever!")

    def __display_save(self):
        print("Game saved!")

    def __display_quit(self):
        print("You quit '%s'! Such a shame." % self.game.title)