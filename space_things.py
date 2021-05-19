from things import Thing


class SolarSystem(Thing):
    def __init__(self, *args, name_seed, star_names, star_types, habitable, num_planets, distance, **kwargs):
        """

        """
        super().__init__(*args, **kwargs)
        self.num_planets = num_planets
        self.name_seed = name_seed
        self.star_names = star_names
        self.star_types = star_types
        self.habitable = habitable
        self.distance = distance
        self.as_dirobj = {"Enter": True, "Leave": True, "Look": True}

    def string(self, print_parts=True):
        # CHANGE THIS!!!

        printable = self.display_name + '\n'
        printable += f'Distance from Earth: {round(self.distance, 2)} light years.\n'
        printable += f'{len(self.star_names)} star{"" if len(self.star_names) == 1 else "s"}: '
        for i, star in enumerate(self.star_names):
            printable += f'{star}, a {self.star_types[i]}; '

        printable += f'\nThis system has {self.num_planets} planet{"" if self.num_planets == 1 else "s"}'
        if print_parts:
            printable += ':\n'
            for planet in self.contents.values():
                printable += '- ' + planet.string()
                printable += '\n'
        return printable

    def _on_enter(self, **kwargs):
        self.entity_state["Entered"] = True
        if self.action_description["Enter"]:
            return self.action_description["Enter"]
        else:
            return f'You just entered the System {self.display_name}.'

    def _on_leave(self, **kwargs):
        self.is_known = False
        return f"You're leaving behind {self.display_name}, as you look for other worlds to settle!"


class Planet(Thing):
    """

    """
    def __init__(self, *args, planet_type, num_satellites, temperature,
                 rocky_planet_type, water_type, atmosphere_type, lifeforms,
                 dangerous_lifeforms, colonizable, **kwargs):
        super().__init__(*args, **kwargs)

        self.planet_type = planet_type
        self.num_satellites = num_satellites
        self.temperature = temperature
        self.rocky_planet_type = rocky_planet_type
        self.water_type = water_type
        self.atmosphere_type = atmosphere_type
        self.lifeforms = lifeforms
        self.dangerous_lifeforms = dangerous_lifeforms
        self.colonizable = colonizable

    def __str__(self):
        return self.display_name + ': '

    def string(self, print_parts=True):
        printable = str(self)
        printable += f'{self.planet_type}, {self.temperature}, {self.rocky_planet_type}, {self.water_type},' \
                     f' {self.atmosphere_type}, {self.lifeforms}, {self.dangerous_lifeforms},' \
                     f' {self.colonizable}'
        return printable

    def _on_look(self, **kwargs):
        pass







