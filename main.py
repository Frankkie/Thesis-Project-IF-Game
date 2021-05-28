import threading
from app import MyApp
from init_all import Initializer
import sys


class GameThread(threading.Thread):
    """

    """
    def __init__(self, replay=False, **kwargs):
        super().__init__()
        self.init = Initializer()
        self.replay = replay

    def run(self):
        if self.replay:
            self.init.replay_game()
        else:
            self.init.load_game()


answer = input("REPLAY? (y/n): ")
if answer == "y":
    replay = True
else:
    replay = False

init = GameThread(replay=replay)

MyApp(init).run()

sys.exit(0)
