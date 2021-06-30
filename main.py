import threading
from init_all import Initializer
from app import MyApp

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


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

