

class Display:
    def __init__(self, game):
        self.game = game
        self.text = None

    def display(self, text, text_type):
        self.text = text
        if text_type == "Error":
            self.__display_error(text)
        elif text_type == "Initial":
            self.__display_init()
        elif text_type == "Prompt":
            self.__display_prompt()
        elif text_type == "AfterAction":
            for sent in self.text:
                for res in sent:
                    if res[1] == "action":
                        self.__display_action(res[0])
                    elif res[1] == "error":
                        self.__display_error(res[0])
                    elif res[1] == "dialog":
                        self.__display_dialog(res[0])
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
        for r in text[1]:
            print(r)
        print()

    def __display_chapter_event(self):
        if not self.text["Descriptions"]:
            return
        for result in self.text["Descriptions"]:
            print(result)
        print()

    def __display_init(self):
        print(self.game.title)
        print(self.game.credits)
        print("\n")

    def __display_help(self):
        print("No one can help you!")
        print("\n")

    def __display_undo(self):
        print("Mistakes are forever!")
        print("\n")

    def __display_save(self):
        print("Game saved!")
        print("\n")

    def __display_quit(self):
        print("You quit '%s'! Such a shame." % self.game.title)
        print("\n")

    def __display_replay(self):
        print("> " + self.text)
