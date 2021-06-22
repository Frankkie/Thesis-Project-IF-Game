from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader, Sound
from numpy import random
import os

FontSize = 20
FontName = 'Invasion2000'

songs = ['Resurrection.WAV', 'Resurrection2.WAV', 'Belaya Noch.WAV', 'Na Zare.WAV']


class GamePage(GridLayout):
    def __init__(self, init_object, app, **kwargs):
        super().__init__(**kwargs)
        self.rows = 4
        self.rows_minimum = {0: Window.size[1] * 0.35, 1: Window.size[1] * 0.1, 2: Window.size[1] * 0.1,
                             3: Window.size[1] * 0.45}
        self.cols = 3
        self.game = None
        self.init_object = init_object
        self.app = app
        self.current_command = None
        self.command_history = []
        self.command_history_index = 0
        self.history = None
        self.new_command = None
        self.send = None
        self.command_sent = True
        self.pause_music = False
        self.song = None
        self.songs = [SoundLoader.load(os.path.join('Assets', song)) for song in songs]
        self.placeholders = [Label() for i in range(9)]
        self.start_label = Label(text=('Press Start to begin a new game.\nPress Replay to play the a previous one.\n' +
                                       'Press the Right Alt key to stop and start music.\n' +
                                       'Write qu to quit the game.\n'),
                                 font_size=FontSize + 10, font_name=FontName,
                                 color='bb3333')
        
        self.start_label.text_size = (Window.size[0] * 0.5, None)
        self.start_label.texture_size = (Window.size[0] * 0.5, None)

        self.start_button = Button(text="Start", font_size=FontSize + 20, font_name=FontName,
                                   height=Window.size[1] * 0.1, width=Window.size[0] * 0.3,
                                   background_color='aa0000')
        self.start_button.bind(on_press=self.start_game)
        self.replay_button = Button(text="Replay", font_size=FontSize + 20, font_name=FontName,
                                    height=Window.size[1] * 0.1, width=Window.size[0] * 0.3,
                                    background_color='aa0000')
        self.replay_button.bind(on_press=self.replay_game)

        self.add_widget(self.placeholders[6])
        self.add_widget(self.placeholders[7])
        self.add_widget(self.placeholders[8])

        self.add_widget(self.placeholders[2])
        self.add_widget(self.start_button)
        self.add_widget(self.placeholders[3])

        self.add_widget(self.placeholders[4])
        self.add_widget(self.replay_button)
        self.add_widget(self.placeholders[5])

        self.add_widget(self.placeholders[0])
        self.add_widget(self.start_label)
        self.add_widget(self.placeholders[1])

    def start_game(self, _):
        self.init_object.replay = False
        self.place_widgets()
        while not self.init_object.init.game:
            pass
        self.game = self.init_object.init.game
        self.game.app = self.app
        self.play_next_song()

    def replay_game(self, _):
        self.place_widgets()
        while not self.init_object.init.game:
            pass
        self.game = self.init_object.init.game
        self.game.replay = True
        self.game.app = self.app
        self.play_next_song()

    def place_widgets(self):
        self.remove_widget(self.start_button)
        self.remove_widget(self.replay_button)
        self.remove_widget(self.start_label)
        for widget in self.placeholders:
            self.remove_widget(widget)

        self.cols = 1
        self.rows = 2

        self.history = ScrollableLabel(height=Window.size[1] * 0.9, size_hint_y=None)
        self.add_widget(self.history)

        self.new_command = TextInput(width=Window.size[0] * 0.8, size_hint_x=None, multiline=False,
                                     font_size=FontSize + 10, font_name=FontName,
                                     foreground_color='33ff33',
                                     background_color='333333')
        self.send = Button(text="Command", font_size=FontSize + 10, font_name=FontName, background_color='aa0000')
        self.send.bind(on_press=self.send_command)
        bottom_line = GridLayout(cols=2)
        bottom_line.add_widget(self.new_command)
        bottom_line.add_widget(self.send)
        self.add_widget(bottom_line)

        Window.bind(on_key_down=self.on_key_down)

        Clock.schedule_once(self.focus_text_input, 0.1)
        Clock.schedule_interval(self.update_layout, 1)
        self.bind(size=self.adjust_fields)

    def send_command(self, _):
        command = self.new_command.text
        self.current_command = command
        self.command_history.append(command)
        self.command_history_index = len(self.command_history)
        self.new_command.text = ''
        self.game.display.print_on_screen(command, color=self.game.display.prompt_color)
        Clock.schedule_once(self.focus_text_input, 0.1)

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:
            self.send_command(None)

        # Up arrow, show history
        if keycode == 82:
            self.command_history_index -= 1
            if self.command_history_index < 0:
                self.command_history_index = 0
                return
            if self.command_history_index >= len(self.command_history):
                self.new_command.text = ''
                self.command_history_index = len(self.command_history)
            try:
                command = self.command_history[self.command_history_index]
                self.new_command.text = command.rstrip()
            except IndexError:
                pass

        # Down arrow
        if keycode == 81:
            self.command_history_index += 1
            if self.command_history_index < 0:
                self.command_history_index = 0
                return
            if self.command_history_index >= len(self.command_history):
                self.new_command.text = ''
                self.command_history_index = len(self.command_history)
            try:
                command = self.command_history[self.command_history_index]
                self.new_command.text = command.rstrip()
            except IndexError:
                pass
            
        # AltGr
        if keycode == 230:
            if not self.pause_music:
                self.pause_music = True
                self.song.stop()
            else:
                self.pause_music = False
                self.play_next_song()

    def focus_text_input(self, _):
        self.new_command.focus = True

    def update_layout(self, _=None):
        if self.command_sent:
            self.history.update_game_history_layout()
            self.history.custom_scroll_to()
            self.command_sent = False

    def adjust_fields(self, *_):
        if Window.size[1] * 0.1 < 50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1] * 0.9
        self.history.height = new_height

        if Window.size[0] * 0.2 < 160:
            new_width = Window.size[0] - 160
        else:
            new_width = Window.size[0] * 0.8
        self.new_command.width = new_width

        Clock.schedule_once(self.history.update_game_history_layout, 0.05)

    def on_stop(self, _):
        if not self.pause_music:
            self.play_next_song()

    def play_next_song(self):
        self.song = random.choice(self.songs)
        Sound.bind(self.song, on_stop=self.on_stop)
        self.song.volume = 0.2
        self.song.play()

    def stop_music(self):
        if not self.pause_music:
            self.pause_music = True
            self.song.stop()


class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        self.game_history = Label(size_hint_y=None, markup=True, font_size=FontSize, font_name=FontName)
        self.scroll_to_point = Label()

        self.layout.add_widget(self.game_history)
        self.layout.add_widget(self.scroll_to_point)

    def update_game_history(self, message):
        try:
            if self.game_history.text[-2:] == '\n\n' and message[0] == '\n':
                self.game_history.text += message[1:]
            else:
                self.game_history.text += message
        except IndexError:
            self.game_history.text += message
        self.parent.command_sent = True

    def update_game_history_layout(self, _=None):
        self.game_history._label.refresh()
        self.layout.height = self.game_history._label.texture.size[1] + 15
        self.game_history.height = self.game_history._label.texture.size[1]
        self.game_history.text_size = (self.game_history.width * 0.98, None)
        self.custom_scroll_to()

    def custom_scroll_to(self):
        if self.layout.height > Window.height * 0.9:
            self.scroll_to(self.scroll_to_point)
