from numpy import random
from planet_room_generator import PlanetRoomGenerator


class Chapter:
    def __init__(self, key, title, intro_description, outro_description, map_files, first_room=None,
                 convonodes_files=None, dialogevents_files=None, events_files=None, topics_files=None,
                 end_conditions=None, chapter_state=None, alternate_intro=None):
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
        self.alternate_intro = alternate_intro

    def start_chapter(self, game, replay=False):
        """
        This method is triggered by the game at the start of a Chapter, and returns the introduction
        description of the chapter, based on the previous Chapter.
        :return: None
        """
        if self.alternate_intro:
            if 'is known' in self.chapter_state.keys():
                descr = self.alternate_intro
            else:
                descr = self.intro_description
        else:
            descr = self.intro_description
        game.display.queue(descr, "ChapterStart")
        self.chapter_state['is known'] = True
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
            if self._eval_conditions(game, conditions):
                res = self._end_chapter(chapter_key)
                game.display.queue(res, "ChapterEvent")
                next_chapter = chapter_key
                return next_chapter

        return next_chapter

    def _eval_conditions(self, game, conditions):
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
                for sentence in self.intro_description:
                    game.display.queue(sentence, "ChapterStart")
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

            game.display.queue('Skip help? (y/n)', 'Prompt')
            game.display.output()
            answer = game.display.fetch()
            if answer != 'y':
                for sentence in self.help_description:
                    game.display.queue(sentence, 'Help')
                game.display.output()

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
        game.game_state['lose'] = True
        game.display.queue(self.intro_description, "ChapterStart")
        game.display.queue(self.outro_description, "ChapterEvent")
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
        game.game_state['win'] = True
        game.display.queue(self.intro_description, "ChapterStart")
        game.display.queue(self.outro_description, "ChapterEvent")
        return next_chapter


class SpaceChapter(Chapter):
    """
    This is a chapter type that is triggered when the PC's fleet is in Outer Space.
    """

    def __init__(self, *args, sol_time=0, last_sol_time=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.sol_time = sol_time
        self.last_sol_time = last_sol_time
        if 'solar systems' not in self.chapter_state.keys():
            self.chapter_state['solar systems'] = 0

    def advance_chapter(self, game):
        """
        This method loops through possible Chapter events and end triggers to evaluate
        the next event of the Chapter. It also creates a new Solar System, if it is
        timed to do so.

        :param game:
            the game object that has triggered the chapter
        :return:
            dictionary of info about the events triggered.

        """
        next_chapter = None

        res = self.new_solar_system(game)
        if res:
            game.display.queue(res, "ChapterEvent")

        for event in game.events.values():
            if event.eval_conditions(game):
                res = event.trigger(game)
                game.display.queue(res, "ChapterEvent")

        try:
            current_system_key = game.game_state['current system']
        except KeyError:
            current_system_key = None
        if current_system_key:
            solarsystem = game.things[current_system_key]
            try:
                if solarsystem.entity_state["Entered"]:
                    next_chapter = "SolarSystemChapter"
            except KeyError:
                pass
        return next_chapter

    def new_solar_system(self, game):
        try:
            current_system_key = game.game_state['current system']
        except KeyError:
            current_system_key = None

        chapter_time = game.game_state['chapter time']
        if current_system_key:
            current_system = game.things[current_system_key]
            if not current_system.is_known:
                del game.things[current_system.key]
                game.game_state['current system'] = None
                self.last_sol_time = chapter_time
            else:
                return None

        if chapter_time >= (self.sol_time + self.last_sol_time):
            system = game.solar_system_gen.generate_systems(self.chapter_state['solar systems'])

            game.things[system.key] = system
            game.game_state['current system'] = system.key
            game.refresh_things()
            self.chapter_state['solar systems'] += 1
            if self.chapter_state['solar systems'] == 1:
                return f"'Admiral, Sir! We're approaching our first alien system, {system.display_name}!'\n" \
                       "'We can either enter it or leave it, or even go to the telescope room and take a closer look!'"
            else:
                return f"'Sir, I must notify you that we're approaching a new solar system, {system.display_name}!'"
        else:
            return None


class SolarSystemChapter(Chapter):
    """
    This is a chapter type that is triggered when the PC's fleet enters a solar system.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_chapter(self, game, replay=False):
        """
        This method is triggered by the game at the start of a Chapter, and returns the introduction
        description of the chapter, based on the previous Chapter.

        :return: None

        """
        solarsystem = game.things[game.game_state['current system']]
        game.solar_system_gen.generate_descriptions(solarsystem)
        num_stars = len(solarsystem.star_types)
        num_planets = solarsystem.num_planets
        system_name = solarsystem.key

        intro = None
        if self.alternate_intro:
            if 'is known' in self.chapter_state.keys():
                intro = self.alternate_intro
        self.chapter_state['is known'] = True
        if not intro:
            random.seed(solarsystem.name_seed)
            intro = random.choice(self.intro_description)
        intro = intro.format(star_plural='s' if num_stars > 1 else '',
                             num_planets=num_planets, system_name=system_name)
        game.display.queue(intro, "ChapterStart")

        return None

    def advance_chapter(self, game):
        """
        This method loops through possible Chapter events and end triggers to evaluate
        the next event of the Chapter.

        :param game:
            the game object that has triggered the chapter
        :return:
            dictionary of info about the events triggered.

        """
        next_chapter = None

        for event in game.events.values():
            if event.eval_conditions(game):
                res = event.trigger(game)
                game.display.queue(res, "ChapterEvent")

        current_system_key = game.game_state['current system']

        if current_system_key:
            solarsystem = game.things[current_system_key]
            if not solarsystem.entity_state["Entered"]:
                del game.things[solarsystem.key]
                game.game_state['current system'] = None
                next_chapter = "Deep Space"

            for planet_key in solarsystem.contents.keys():
                planet = solarsystem.contents[planet_key]['obj']
                try:
                    if planet.entity_state["Landed"]:
                        game.game_state['current planet'] = planet_key
                        next_chapter = "PlanetChapter"
                except KeyError:
                    pass

        if next_chapter:
            game.display.queue(self.outro_description[next_chapter], "ChapterEvent")
        return next_chapter


class PlanetChapter(Chapter):
    """
    This is a chapter type that is triggered when the PC's fleet lands on a planet in a solar system.
    """

    def __init__(self, *args, last_room=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not last_room:
            last_room = self.first_room
        self.last_room = last_room

    def start_chapter(self, game, replay=False):
        """
        This method is triggered by the game at the start of a Chapter, and returns the introduction
        description of the chapter, based on the previous Chapter.

        :return: Next_chapter

        """
        planet = game.things[game.game_state['current planet']]
        solarsystem = game.things[game.game_state['current system']]
        # 0. Generate landing description
        game.display.queue(self.intro_description, "ChapterStart")
        if planet.rocky_planet_type != 'Rocky Planet':
            next_chapter = "Death"
            return next_chapter
        # 1. Generate LANDING SPOT ROOM
        game.solar_system_gen.generate_landing_spot(game, solarsystem, planet)
        # 2. Generate planet threat
        # 3. Generate planet rooms
        # 4. Generate colony object

    def advance_chapter(self, game):
        """
        This method loops through possible Chapter events and end triggers to evaluate
        the next event of the Chapter.

        :param game:
            the game object that has triggered the chapter
        :return:
            dictionary of info about the events triggered.

        """
        next_chapter = None
        planet = None

        for condition_set in self.end_conditions:
            conditions = condition_set["conditions"]
            chapter_key = condition_set["next chapter"]
            if self._eval_conditions(game, conditions):
                res = self._end_chapter(chapter_key)
                game.display.queue(res, "ChapterEvent")
                next_chapter = chapter_key
                return next_chapter

        if not next_chapter:
            planet_key = game.game_state['current planet']
            planet = game.things[planet_key]
            if not planet.entity_state["Landed"]:
                game.game_state['current planet'] = None
                self.map_files = ['t0p0']
                next_chapter = "SolarSystemChapter"

        if planet is not None:
            solarsystem = game.things[game.game_state['current system']]
            current_room_key = game.game_state['current room']
            if current_room_key != self.last_room:
                game.solar_system_gen.generate_planet_rooms(game, solarsystem, planet)
            self.last_room = current_room_key

        if next_chapter and next_chapter != 'ColonyChapter':
            game.display.queue(self.outro_description[next_chapter], "ChapterEvent")

        elif not next_chapter:
            for event in game.events.values():
                if event.eval_conditions(game):
                    res = event.trigger(game)
                    game.display.queue(res, "ChapterEvent")

        return next_chapter


class ColonyChapter(Chapter):
    """
    This is a chapter type that is triggered when the PC sets up a Colony on a planet.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_chapter(self, game, replay=False):
        """
        This method is triggered by the game at the start of a Chapter, and returns the introduction
        description of the chapter, based on the previous Chapter.
        :return: None
        """
        planet = game.things[game.game_state['current planet']]
        game.game_state['colonizable'] = planet.colonizable
        game.display.queue(self.intro_description, "ChapterStart")
        next_chapter = self.advance_chapter(game)
        print(self.end_conditions[0]["conditions"][0].eval_condition(game))
        return next_chapter
