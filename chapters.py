

class Chapter:
    def __init__(self, key, title, intro_description, outro_description, map_files, first_room,
                 convonodes_files=None, dialogevents_files=None, events_files=None, topics_files=None,
                 end_conditions=None, chapter_state=None):
        """

        :param key:
        :param title:
        :param intro_description:
        :param outro_description:
        :param map_files:
        :param first_room:
        :param convonodes_files:
        :param dialogevents_files:
        :param events_files:
        :param topics_files:
        :param end_conditions:
        :param chapter_state:
        """
        self.key = key
        self.title = title
        self.intro_description = intro_description
        self.outro_description = outro_description
        self.first_room = first_room

        if not convonodes_files:
            convonodes_files = []
        if not dialogevents_files:
            dialogevents_files = []
        if not events_files:
            events_files = []
        if not map_files:
            map_files = []
        if not topics_files:
            topics_files = []

        self.convonodes_files = convonodes_files
        self.dialogevents_files = dialogevents_files
        self.events_files = events_files
        self.map_files = map_files
        self.topics_files = topics_files

        if not end_conditions:
            end_conditions = {}
        self.end_conditions = end_conditions

        if not chapter_state:
            chapter_state = {}
        self.chapter_state = chapter_state

    def start_chapter(self, game, replay=False):
        """
        This method is triggered by the game at the start of a Chapter, and returns the introduction
        description of the chapter, based on the previous Chapter.
        :return: None
        """
        game.display.queue(self.intro_description, "ChapterStart")
        return None

    def advance_chapter(self, game):
        """
        This method loops through possible Chapter events and end triggers to evaluate
        the next event of the Chapter.
        :param game: the game object that has triggered the chapter
        :return: dictionary of info about the events triggered.
        """
        next_chapter = None

        for event in game.events.values():
            if event.eval_conditions(game):
                res = event.trigger(game)
                game.display.queue(res, "ChapterEvent")

        for condition_set in self.end_conditions:
            conditions = condition_set["conditions"]
            chapter_key = condition_set["next chapter"]
            if self.__eval_conditions(game, conditions):
                res = self._end_chapter(chapter_key)
                game.display.queue(res, "ChapterEvent")
                next_chapter = chapter_key
                return next_chapter

        return next_chapter

    def __eval_conditions(self, game, conditions):
        """
        This method evaluates the conditions for the end of the chapter.
        :param game: The game object.
        :param conditions: A list of Condition Objects.
        :return: Bool, True if all the conditions are satisfied, False otherwise
        """
        for cond in conditions:
            if not cond.eval_condition(game):
                return False
        return True

    def _end_chapter(self, next_chapter):
        """
        This method returns the outro description of this Chapter, depending on the next chapter.
        :param next_chapter: The key of the next chapter.
        :return: String
        """
        if next_chapter in self.outro_description.keys():
            result = self.outro_description[next_chapter]
            return result
        else:
            result = self.outro_description['generic']
            return result

    def to_json(self):
        """
           Convert the instance of this class to json
        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = self.__class__.__name__
        return obj_dict


class IntroChapter(Chapter):
    """
    This is always the first Chapter of a game. Only one IntroChapter can exist in the Game Folder.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class IntroChapterUnionColonizer(IntroChapter):
    """
        This is always the first Chapter of the Union Colonizer game.
        """

    def __init__(self, *args, help_description, **kwargs):
        super().__init__(*args, **kwargs)
        self.help_description = help_description

    def start_chapter(self, game, replay=False):
        """
        This method is triggered by the game at the start of the Union Colonizer game.
        :return: None
        """

        if not replay:
            game.display.queue('Skip intro? (y/n)', 'Prompt')
            game.display.output()
            answer = game.display.fetch()
            if answer != 'y':
                game.display.queue(self.intro_description, "ChapterStart")
                game.display.output()

            game.display.queue('Skip help? (y/n)', 'Prompt')
            game.display.output()
            answer = game.display.fetch()
            if answer != 'y':
                game.display.queue(self.help_description, 'Help')
                game.display.output()

            import re
            name = None
            year = None
            while name is None:
                game.display.queue('What is your name? ', 'Prompt')
                game.display.output()
                answer = game.display.fetch()
                if re.match("^[a-zA-Z ,.'-]+$", answer):
                    name = answer

            while year is None:
                game.display.queue(f'What year where you born in, Admiral {name}? ', 'Prompt')
                game.display.output()
                answer = game.display.fetch()
                try:
                    answer = int(answer)
                except ValueError:
                    continue
                if answer > 2040:
                    game.display.queue('Please give me a year before 2040.', 'Error')
                    game.display.output()
                elif answer < 2000:
                    game.display.queue('Please give me a year after 1999.', 'Error')
                    game.display.output()
                else:
                    year = answer

            game.seed = self.__hash_answers(name, year)

        return "Deep Space"

    def __hash_answers(self, name, year):
        res = 1
        for c in list(name):
            res *= (ord(c) + 1)
        res = int(res/year)
        res = res % (10**8)
        return res


class EndChapter(Chapter):
    """
    This is always the last Chapter of a game. Only one EndChapter can exist in the Game Folder.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_chapter(self, game, replay=False):
        """
        The End Chapter is over before it had a chance to finish.
        Thus, the End Chapter's start_chapter method returns its outro description right away.

        :return: str, Chapter Key
            The next chapter of the game.

        """
        next_chapter = "__END__"

        game.display.queue(self.intro_description, "ChapterStart")
        game.display.queue(self._end_chapter("__END__"), "ChapterEvent")
        return next_chapter


class DeathChapter(Chapter):
    """
    This is a Chapter that is triggered when the PC dies.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_chapter(self, game, replay=False):
        """
        The Death Chapter is over before it had a chance to finish.

        :return: str, Chapter Key
            The next chapter of the game.

        """
        next_chapter = "End"

        game.display.queue(self.intro_description, "ChapterStart")
        return next_chapter


class WinChapter(Chapter):
    """
    This is the Chapter that is triggered when the PC wins.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_chapter(self, game, replay=False):
        """
        The Win Chapter is over before it had a chance to finish.

        :return: str, Chapter Key
            The next chapter of the game.

        """
        next_chapter = "End"

        game.display.queue(self.intro_description, "ChapterStart")
        return next_chapter


class SpaceChapter(Chapter):
    """
    This is a chapter type that is triggered when the PC's fleet is in Outer Space.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SolarSystemChapter(Chapter):
    """
    This is a chapter type that is triggered when the PC's fleet enters a solar system.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PlanetChapter(Chapter):
    """
    This is a chapter type that is triggered when the PC's fleet lands on a planet in a solar system.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ColonyChapter(Chapter):
    """
    This is a chapter type that is triggered when the PC sets up a Colony on a planet.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



