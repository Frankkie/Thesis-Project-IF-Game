from things import Thing


class SolarSystem(Thing):
    def __init__(self, *args, star_names, star_types, habitable, num_planets, **kwargs):
        """

        """
        super().__init__(*args, **kwargs)
        self.num_planets = num_planets
        self.star_names = star_names
        self.star_types = star_types
        self.habitable = habitable

    def __str__(self):
        # CHAGE THIS
        return self.display_name + '\n'

    def string(self, print_parts=True):
        # CHANGE THIS!!!

        printable = str(self)
        printable += f'{len(self.star_names)} star{"" if len(self.star_names) == 1 else "s"}: '
        for i, star in enumerate(self.star_names):
            printable += f'{star}, a {self.star_types[i]}; '

        printable += f'\nThis system has {self.num_planets} planet{"" if self.num_planets == 1 else "s"}.'
        if print_parts:
            for planet in self.contents.keys():
                printable += '- ' + planet
        return printable

    def _on_look(self, **kwargs):
        pass

    def _on_enter(self, **kwargs):
        pass

    def _on_leave(self, **kwargs):
        pass







