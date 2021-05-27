import time
import threading


class CustomTimer(threading.Thread):
    """

    """
    def __init__(self, game, *args, pause=True, **kwargs):
        super().__init__()
        self.game = game
        self.args = args
        self.pause = pause
        self.stopped = False
        self.kwargs = kwargs

    def run(self):
        while True:
            if self.pause:
                continue
            if self.stopped:
                return
            time.sleep(0.1)
            self.game.game_state['game time'] += 0.1
            self.game.game_state['chapter time'] += 0.1

    def set_timer(self, game_time=None, chapter_time=None):
        if game_time:
            self.game.game_state['game time'] = game_time
        if chapter_time:
            self.game.game_state['chapter time'] = chapter_time




