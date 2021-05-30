import threading
from init_all import Initializer
from app import MyApp


class GameThread(threading.Thread):
    """

    """
    def __init__(self, replay=False, **kwargs):
        super().__init__()
        self.init = Initializer()
        self.replay = replay

    def run(self):
        self.init.load_game(self.replay)


MyApp(GameThread()).run()

