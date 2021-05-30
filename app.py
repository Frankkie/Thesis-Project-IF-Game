from kivy.core.window import Window

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase

import os

from game_screen import GamePage

Window.size = (1200, 700)

window_color = (60/255, 57/255, 60/255, 1)
Window.clearcolor = window_color

LabelBase.register(name='lunchds',
                   fn_regular=os.path.join('Assets', 'lunchds.ttf'))
LabelBase.register(name='SF Atarian System',
                   fn_regular=os.path.join('Assets', 'SF Atarian System.ttf'))
LabelBase.register(name='Invasion2000',
                   fn_regular=os.path.join('Assets', 'invasion2000.regular.ttf'))


class MyApp(App):
    def __init__(self, init_object, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        init_object.start()
        self.sm = ScreenManager()
        screen = Screen(name='Main')
        self.game = None
        self.game_screen = GamePage(init_object, self)
        screen.add_widget(self.game_screen)
        self.sm.add_widget(screen)
        Window.bind(on_request_close=self.exit_check)

    def build(self):
        self.title = "Union Colonizer"
        return self.sm

    def exit_check(self, *args):
        if not self.game:
            return False

        if not self.game.quit:
            return True
        else:
            self.game_screen.player.pause = True
            return False
