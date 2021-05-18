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
        try:
            start_game = self.kwargs['start_game']
        except KeyError:
            start_game = 0
        try:
            start_chapter = self.kwargs['start_chapter']
        except KeyError:
            start_chapter = 0

        self.game.game_state['game time'] = start_game
        self.game.game_state['chapter time'] = start_chapter
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




