from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

FontSize = 25
FontName = 'SF Atarian System'


class GamePage(GridLayout):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)

        self.game = game
        self.current_command = None

        # We are going to use 1 column and 2 rows
        self.cols = 1
        self.rows = 2

        # First row is going to be occupied by our scrollable label
        # We want it be take 90% of app height
        self.history = ScrollableLabel(height=Window.size[1] * 0.9, size_hint_y=None)
        self.add_widget(self.history)

        self.new_command = TextInput(width=Window.size[0] * 0.8, size_hint_x=None, multiline=False,
                                     font_size=FontSize+10, font_name=FontName)
        self.send = Button(text="Command", font_size=FontSize+10, font_name=FontName)
        self.send.bind(on_press=self.send_command)

        bottom_line = GridLayout(cols=2)
        bottom_line.add_widget(self.new_command)
        bottom_line.add_widget(self.send)
        self.add_widget(bottom_line)

        # To be able to send message on Enter key, we want to listen to keypresses
        Window.bind(on_key_down=self.on_key_down)

        # We also want to focus on our text input field
        # Kivy by default takes focus out out of it once we are sending message
        # The problem here is that 'self.new_command.focus = True' does not work when called directly,
        # so we have to schedule it to be called in one second
        # The other problem is that schedule_once() have no ability to pass any parameters, so we have
        # to create and call a function that takes no parameters
        Clock.schedule_once(self.focus_text_input, 1)
        self.bind(size=self.adjust_fields)

    # Gets called when either Send button or Enter key is being pressed
    # (kivy passes button object here as well, but we don;t care about it)
    def send_command(self, _):
        # Get message text and clear message input field
        command = self.new_command.text
        self.current_command = command
        self.new_command.text = ''
        self.game.display.print_on_screen(command, color='54a6ff')
        # self.history.update_game_history(f"[color='54a6ff']{command}[/color]")
        # As mentioned above, we have to shedule for refocusing to input field
        Clock.schedule_once(self.focus_text_input, 0.1)

    # Gets called on key press
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # But we want to take an action only when Enter key is being pressed, and send a message
        if keycode == 40:
            self.send_command(None)

    # Sets focus to text input field
    def focus_text_input(self, _):
        self.new_command.focus = True
        self.history.custom_scroll_to()
        self.history.update_game_history_layout()

    # Updates page layout
    def adjust_fields(self, *_):
        # Game history height - 90%, but at least 50px for bottom new message/send button part
        if Window.size[1] * 0.1 < 50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1] * 0.9
        self.history.height = new_height

        # New message input width - 80%, but at least 160px for send button
        if Window.size[0] * 0.2 < 160:
            new_width = Window.size[0] - 160
        else:
            new_width = Window.size[0] * 0.8
        self.new_command.width = new_width

        # Update game history layout
        # self.history.update_game_history_layout()
        Clock.schedule_once(self.history.update_game_history_layout, 0.05)


# This class is an improved version of Label
# Kivy does not provide scrollable label, so we need to create one
class ScrollableLabel(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ScrollView does not allow us to add more than one widget, so we need to trick it
        # by creating a layout and placing two widgets inside it
        # Layout is going to have one collumn and and size_hint_y set to None,
        # so height wo't default to any size (we are going to set it on our own)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        # Now we need two widgets - Label for game history and 'artificial' widget below
        # so we can scroll to it every new message and keep new messages visible
        # We want to enable markup, so we can set colors for example
        self.game_history = Label(size_hint_y=None, markup=True, font_size=FontSize, font_name=FontName)
        self.scroll_to_point = Label()

        # We add them to our layout
        self.layout.add_widget(self.game_history)
        self.layout.add_widget(self.scroll_to_point)

    # Method called externally to add new message to the game history
    def update_game_history(self, message):

        # First add new line and message itself
        try:
            if self.game_history.text[-2:] == '\n\n' and message[0] == '\n':
                self.game_history.text += message[1:]
            else:
                self.game_history.text += message
        except IndexError:
            self.game_history.text += message

        # Set layout height to whatever height of game history text is + 15 pixels
        # (adds a bit of space at teh bottom)
        # Set game history label to whatever height of game history text is
        # Set width of game history text to 98 of the label width (adds small margins)
        self.game_history._label.refresh()
        self.layout.height = self.game_history._label.texture.size[1] + 15
        self.game_history.height = self.game_history._label.texture.size[1]
        self.game_history.text_size = (self.game_history.width * 0.98, None)

        # As we are updating above, text height, so also label and layout height are going to be bigger
        # than the area we have for this widget. ScrollView is going to add a scroll, but won't
        # scroll to the botton, nor is there a method that can do that.
        # That's why we want additional, empty widget below whole text - just to be able to scroll to it,
        # so scroll to the bottom of the layout
        self.custom_scroll_to()

    def update_game_history_layout(self, _=None):
        # Set layout height to whatever height of game history text is + 15 pixels
        # (adds a bit of space at the bottom)
        # Set game history label to whatever height of game history text is
        # Set width of game history text to 98 of the label width (adds small margins)
        self.game_history._label.refresh()
        self.layout.height = self.game_history._label.texture.size[1] + 15
        self.game_history.height = self.game_history._label.texture.size[1]
        self.game_history.text_size = (self.game_history.width * 0.98, None)

    def custom_scroll_to(self):
        if self.layout.height > Window.height * 0.9:
            self.scroll_to(self.scroll_to_point)

