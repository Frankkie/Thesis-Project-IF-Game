from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.core.text import LabelBase

import os

from game_screen import GamePage

Window.size = (1200, 700)
Window.clearcolor = (0.1, 0.1, 0.15, 1)

LabelBase.register(name='lunchds',
                   fn_regular=os.path.join('Assets', 'lunchds.ttf'))
LabelBase.register(name='computer_pixel-7',
                   fn_regular=os.path.join('Assets', 'computer_pixel-7.ttf'))
LabelBase.register(name='SF Atarian System',
                   fn_regular=os.path.join('Assets', 'SF Atarian System.ttf'))


class MyApp(App):
    def __init__(self, init_object, **kwargs):
        super(MyApp, self).__init__(**kwargs)

        init_object.start()
        self.init_object = init_object
        self.sm = ScreenManager()
        screen = Screen(name='Main')
        self.game = None
        self.game_screen = GamePage(None)
        screen.add_widget(self.game_screen)
        self.sm.add_widget(screen)

    def build(self):
        self.title = "Union Colonizer"
        while not self.game:
            self.game = self.init_object.init.game
        self.game.app = self
        return self.sm

    def on_request_close(self, *args):
        print("here")
        self.game.quit_game()
        return False
