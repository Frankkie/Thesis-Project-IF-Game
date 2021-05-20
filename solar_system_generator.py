import numpy as np
import json
import os

from name_generator import NameGenerator
from space_things import SolarSystem, Planet


class SolarSystemGenerator:
    """

    """

    def __init__(self, seed):
        self.seed = seed
        self.constellation = choose_constellation(seed)
        self.star_name_gen = NameGenerator(self.seed, 'star_name_grammar.cfg', prefix=self.constellation)
        self.planet_gen = PlanetGenerator(self.seed)
        self.generated = set()
        with open(os.path.join("Generators", (self.__class__.__name__.lower() + '.json')), 'r') as file:
            generator_data = json.load(file)
        self.star_numbers = generator_data['star_numbers']
        self.star_number_weights = generator_data['star_number_weights']
        self.star_types = generator_data['star_types']
        self.star_type_weights = generator_data['star_type_weights']
        self.planet_numbers = generator_data['planet_numbers']
        self.planet_numbers_weights = generator_data['planet_numbers_weights']
        self.distances = [4]

    def generate_systems(self, system_seed):
        name = self.star_name_gen.generate_name(system_seed)
        name_seed = self.hash_system_name(name)

        np.random.seed(name_seed)

        num_stars = np.random.choice(self.star_numbers, p=self.star_number_weights)

        star_names = []
        if num_stars == 1:
            star_names = [name]
        else:
            for i in range(num_stars):
                star_names.append(name + ' ' + chr(ord('a') + i))

        star_types = []
        for i in range(num_stars):
            star_types.append(np.random.choice(self.star_types, p=self.star_type_weights))

        if num_stars > 3:
            habitable = False
        else:
            habitable = False
            for t in star_types:
                if t in ['Yellow Dwarf', 'Red Dwarf']:
                    habitable = True
                    break

            for t in star_types:
                if t not in ['Yellow Dwarf', 'Red Dwarf', 'Black Hole', 'Brown Dwarf']:
                    habitable = False
                    break

        num_planets = np.random.choice(self.planet_numbers, p=self.planet_numbers_weights)

        if num_planets == 0:
            habitable = False

        distance = self.distances[-1] + np.random.exponential(scale=5.0)
        self.distances.append(distance)

        sl = SolarSystem(key=name, reference_noun='system', display_name=name, reference_adjectives=['solar', name],
                         star_names=star_names, star_types=star_types, habitable=habitable, num_planets=num_planets,
                         distance=distance, name_seed=name_seed, is_known=True)
        self.planet_gen.generate_planets(sl)
        self.generate_telescope_description(sl)
        return sl

    def hash_system_name(self, name):
        system_seed = 1
        for c in list(name):
            system_seed *= (ord(c) + 1)
        system_seed /= 10000
        system_seed = int(system_seed) % (10 ** 8)
        if system_seed in self.generated:
            return self.hash_system_name(name + 'a')
        self.generated.add(system_seed)
        return system_seed

    def generate_telescope_description(self, solar_system):
        descr = solar_system.string() + '\n'
        planets = [planet['obj'] for planet in solar_system.contents.values()]
        planet_names = [planet.display_name for planet in planets]
        planet_types = [planet.planet_type for planet in planets]

        for i, name in enumerate(planet_names):
            descr += f"- {name}, {planet_types[i]}.\n"

        if len(solar_system.star_names) > 3:
            descr += "The systems' many stars seem to be pulling on its planets in random ways, " \
                     "generating highly elliptical orbits.\n"
        if 'Blue Giant' in solar_system.star_types or 'Red Giant' in solar_system.star_types:
            descr += "The system is obviously dominated by its most Giant star, " \
                     "casting incredible amounts of radiation everywhere.\n"
        if 'White Dwarf' in solar_system.star_types\
                or 'Black Hole' in solar_system.star_types\
                or 'Neutron Star' in solar_system.star_types:
            descr += "The remnants of a long gone star are present here, indicating a violent past.\n"
        if 'Blue Giant' not in solar_system.star_types\
                and 'Read Giant' not in solar_system.star_types\
                and 'Yellow Dwarf' not in solar_system.star_types\
                and 'Red Dwarf' not in solar_system.star_types:
            descr += "The system is barely lit by its dim 'stars'."
        solar_system.action_description['On Use telescope'] = descr


class PlanetGenerator:
    """

    """

    def __init__(self, seed):
        self.seed = seed
        self.star_name_gen = NameGenerator(self.seed, 'planet_name_grammar.cfg')
        with open(os.path.join("Generators", (self.__class__.__name__.lower() + '.json')), 'r') as file:
            generator_data = json.load(file)
        self.planet_types = generator_data['planet_types']
        self.planet_types_weights = generator_data['planet_types_weights']
        self.num_satellites = generator_data['num_satellites']
        self.num_satellites_weights = generator_data['num_satellites_weights']
        self.temperature_types = generator_data['temperature_types']
        self.temperature_types_weights = generator_data['temperature_types_weights']
        self.rocky_planet_types = generator_data['rocky_planet_types']
        self.water_types = generator_data['water_types']
        self.atmosphere_types = generator_data['atmosphere_types']
        self.atmosphere_types_weights = generator_data['atmosphere_types_weights']
        self.lifeform_types = generator_data['lifeform_types']
        self.lifeform_types_weights = generator_data['lifeform_types_weights']

    def generate_planets(self, system):
        num_planets = system.num_planets
        system_seed = system.name_seed
        system_habitability = system.habitable

        if num_planets == 0:
            return {}

        planets = {}
        np.random.seed(self.seed + system.name_seed)
        for i in range(num_planets):
            r = np.random.randint(1, 100)
            name = self.star_name_gen.generate_name(system_seed + (i + r)*r)
            planet = dict()
            planet['display_name'] = name
            planet['reference_noun'] = name.lower()
            planet['key'] = name
            planet['container'] = system.key
            planet_type = np.random.choice(self.planet_types, p=self.planet_types_weights)
            planet['planet_type'] = planet_type
            num_satellites = np.random.choice(self.num_satellites, p=self.num_satellites_weights)
            planet['num_satellites'] = num_satellites
            temperature = np.random.choice(self.temperature_types, p=self.temperature_types_weights)
            planet['temperature'] = temperature

            rocky_planet_type = None
            water_type = None
            atmosphere_type = None
            lifeforms = None
            dangerous_lifeforms = False
            habitable = False
            colonizable = False

            if planet_type in {"Super Earth", "Earth-sized", "Small Rocky"}:
                # Rocky Planet Type
                if temperature in {"Hellishly Hot", "Hot"}:
                    rocky_planet_type = "Lava Planet"
                else:
                    rocky_planet_type = 'Rocky Planet'

                if rocky_planet_type != 'Lava Planet':
                    if temperature in {"Frozen", "Icy"}:
                        water_type = "Ice Planet"
                    else:
                        water_type = np.random.choice(["Desert Planet", "Ocean Planet", "Water World"])
                atmosphere_type = np.random.choice(self.atmosphere_types, p=self.atmosphere_types_weights)
                if (temperature in {"Warm", "Temperate", "Cold"} and
                        water_type in {"Ocean Planet", "Water World"} and
                        atmosphere_type in {"Thick Atmosphere", "Cloudy Atmosphere"}):
                    habitable = system_habitability

                if habitable:
                    lifeforms = np.random.choice(self.lifeform_types, p=self.lifeform_types_weights)
                else:
                    lifeforms = np.random.choice(["No Life", "Former Advanced Life"], p=[0.9, 0.1])

                if lifeforms in {"Primordial Life", "Animal Life", "Former Advanced Life"}:
                    dangerous_lifeforms = np.random.choice([True, False])
                elif lifeforms == "Advanced Life":
                    dangerous_lifeforms = True

            if habitable and not dangerous_lifeforms and water_type != 'Water World':
                colonizable = True

            planet['rocky_planet_type'] = rocky_planet_type
            planet['water_type'] = water_type
            planet['atmosphere_type'] = atmosphere_type
            planet['lifeforms'] = lifeforms
            planet['dangerous_lifeforms'] = dangerous_lifeforms
            planet['colonizable'] = colonizable
            planet['examine_description'] = 'Examining this planet further that far away is impossible.\n' \
                                            'You have to enter its parent system to take a closer look.'
            planet['is_known'] = True
            planet['as_dirobj'] = {'Look': True, 'Landon': True}
            planet['as_indobj'] = {'To': True}
            planet['action_description'] = {'On Send': "Sent drones!"}
            planet = Planet(**planet)
            planets[name] = {'obj': planet, 'tags': ['Planet', 'Look', 'Inventory']}

        system.contents = planets

        return planets


def choose_constellation(seed):
    import pandas as pd
    file_path = os.path.join('Generators', 'constellations.csv')
    with open(file_path, 'r') as file:
        constellations = pd.read_csv(file)
    constellations = constellations['Constellation'].to_numpy()
    np.random.seed(seed)
    const = np.random.choice(list(constellations))
    return const
