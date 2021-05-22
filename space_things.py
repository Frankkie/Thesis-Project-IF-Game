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
        printable = f'{self.key}:\n' \
                    f'This system is located {round(self.distance, 2)} light years from Earth.\n' \
                    f'It has {len(self.star_names)} star{"" if len(self.star_names) == 1 else "s"}:\n' \
                    f'{"; ".join([", ".join([star, self.star_types[i]]) for i, star in enumerate(self.star_names)])}'\
                    f'.\n' \
                    f'There are {self.num_planets} planets in the system.'

        return printable

    def _on_enter(self, **kwargs):
        self.entity_state["Entered"] = True
        if self.action_description["Enter"]:
            return self.action_description["Enter"]
        else:
            return f'You just entered the System {self.display_name}.'

    def _on_leave(self, **kwargs):
        self.entity_state["Entered"] = False
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

    def string(self, print_parts=True):
        printable = self.display_name + ':\n'
        printable += self.examine_description + '\n'
        printable += f'{self.planet_type}, {self.temperature}, {self.rocky_planet_type}, {self.water_type},' \
                     f' {self.atmosphere_type}, {self.lifeforms}, {self.dangerous_lifeforms},' \
                     f' {self.colonizable}'
        return printable

    def _on_landon(self, **kwargs):
        self.entity_state['Landed'] = True
        return self.action_description["Landon"].format(name=self.display_name)

    def on_take_off(self, **kwargs):
        self.entity_state['Landed'] = False
        return self.action_description["Takeoff"].format(name=self.display_name)







