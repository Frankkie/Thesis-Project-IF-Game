

class Chapter:
    def __init__(self, key, title, previous_chapter, intro_description, outro_description,
                 events=None, end_conditions=None):
        """

        :param key: string
        :param title: string
        :param previous_chapter: string, chapter key
        :param intro_description: dict, key: chapter key/'generic', value: string
        :param outro_description: dict, key: chapter key/'generic', value: string
        :param events: dict, key: event key, value: Event Object
        :param end_conditions: dict, key: chapter key, value: Dictionary (conditions)
        """
        self.key = key
        self.title = title
        self.previous_chapter = previous_chapter
        self.intro_description = intro_description
        self.outro_description = outro_description
        if not events:
            self.events = {}
        else:
            self.events = events

        if not end_conditions:
            self.end_conditions = {}
        else:
            self.end_conditions = end_conditions

    def start_chapter(self):
        if self.previous_chapter in self.intro_description.keys():
            result = {"Descriptions": [self.intro_description[self.previous_chapter]], "Next Chapter": None}
            return result
        else:
            result = {"Descriptions": [self.intro_description['generic']], "Next Chapter": None}
            return result

    def advance_chapter(self, game):
        """
        This method loops through possible Chapter events and end triggers to evaluate
        the next event of the Chapter.
        :param game: the game object that has triggered the chapter
        :return: dictionary of info about the events triggered.
        """
        result = {"Descriptions": [], "Next Chapter": None}

        for event_key in self.events:
            event = self.events[event_key]
            conditions = event.trigger_conditions
            if self.__eval_conditions(conditions) and not event.done:
                result["Descriptions"].append(self.__trigger_event(event, game))

        for chapter_key in self.end_conditions.keys():
            conditions = self.end_conditions[chapter_key]
            if self.__eval_conditions(conditions):
                result["Descriptions"].append(self.__end_chapter(chapter_key))
                result["Next Chapter"] = chapter_key
                return result

    def __eval_conditions(self, conditions):
        for cond in conditions:
            if not cond.eval_condition():
                return False
        return True

    def __end_chapter(self, next_chapter):
        if next_chapter in self.outro_description.keys():
            result = self.outro_description[next_chapter]
            return result
        else:
            result = self.outro_description['generic']
            return result

    def __trigger_event(self, event, game):
        event.trigger(game)

    def to_json(self):
        """
           convert the instance of this class to json
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



