import threading
from init_all import Initializer
from app import MyApp
import sys


class GameThread(threading.Thread):
    """

    """
    def __init__(self):
        super().__init__()
        self.init = Initializer()
        self.daemon = True

    def run(self):
        self.init.load_game()


MyApp(GameThread()).run()

