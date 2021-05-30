"""

"""


from display import Display
from load import Loader
from game import Game


class Initializer:
    """
    The class that handles the program before a game is launched.
    """

    def __init__(self):
        self.display = Display(None)
        self.loader = None
        self.game = None

    def load_game(self, replay):
        game_name = "Union Colonizer"
        self.loader = Loader(game_name, None)
        dct, game_args = self.loader.load_game(self.display)

        self.game = Game(**dct)
        self.display.game = self.game
        self.game.boot_game(**game_args)




