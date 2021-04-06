"""
    This is the file for the Game class, the class that holds all the important information
    about the game and its state.
"""
import things
import actors
import verbs


class Game:
    def __init__(self, title, credits_, curr_room):
        self.title = title
        self.credits = credits_
        self.current_room = curr_room
        self.actors = []
        self.verbs = []
        self.things = []
        self.rooms = []

    def boot_game(self):
        # Load Verbs, Actors and Things
        # CHANGE THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.actors.append(actors.Actor("I", "you", description="This is you, the player.",
                                        container=CURRENT_GAME.current_room))
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print(self.title)
        print(self.credits)
        # Print boot up description
        begin = input("Do you want to begin? (y/n) ")
        if begin == "y":
            self.start_game()
        else:
            self.quit_game()

    def start_game(self):
        # Print starting description
        return

    def quit_game(self):
        print("You quit '%s'! Such a shame." % self.title)
        return


#############################################################################

CURRENT_GAME = Game("Test Game", "", None)

