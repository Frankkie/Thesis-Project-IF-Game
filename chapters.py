

class Chapter:
    def __init__(self, key, title, intro_description, outro_description, map_file, first_room,
                 convonodes_file=None, dialogevents_file=None, events_file=None, topics_file=None,
                 end_conditions=None, chapter_state=None):
        """

        :param key:
        :param title:
        :param intro_description:
        :param outro_description:
        :param map_file:
        :param first_room:
        :param convonodes_file:
        :param dialogevents_file:
        :param events_file:
        :param topics_file:
        :param end_conditions:
        :param chapter_state:
        """
        self.key = key
        self.title = title
        self.intro_description = intro_description
        self.outro_description = outro_description
        self.first_room = first_room

        self.convonodes_file = convonodes_file
        self.dialogevents_file = dialogevents_file
        self.events_file = events_file
        self.map_file = map_file
        self.topics_file = topics_file

        if not end_conditions:
            end_conditions = {}
        self.end_conditions = end_conditions

        if not chapter_state:
            chapter_state = {}
        self.chapter_state = chapter_state

    def start_chapter(self, game):
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


class EndChapter(Chapter):
    """
    This is always the last Chapter of a game. Only one EndChapter can exist in the Game Folder.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_chapter(self, game):
        """
        The End Chapter is over before it had a chance to finish.
        Thus, the End Chapter's start_chapter method returns its outro description right away.
        :return: Dictionary with the description of the end of the game.
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


class WinChapter(Chapter):
    """
    This is the Chapter that is triggered when the PC wins.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SpaceChapter(Chapter):
    """
    This is a chapter type that is triggered when the PC's fleet is in Outer Space.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SolarSystemChapter(Chapter):
    """
    This is a chapter type that is triggered when the PC's fleet approaches a solar system.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PlanetChapter(Chapter):
    """
    This is a chapter type that is triggered when the PC's fleet approaches a planet in a solar system.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



