import numpy as np
import json
import os

from name_generator import NameGenerator
from space_things import SolarSystem, Planet


class SolarSystemGenerator:
    """

    """

    def __init__(self, seed, constellation):
        self.seed = seed
        self.constellation = constellation
        self.star_name_gen = NameGenerator(self.seed, 'star_name_grammar.cfg', prefix=self.constellation)
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
            planet['reference_noun'] = name
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

            planet = Planet(**planet)
            planets[name] = {'obj': planet, 'tags': ['Planet', 'Look']}

        system.contents = planets
        # print(system.contents)

        return planets


if __name__ == '__main__':
    gen = SolarSystemGenerator(1998, 'Cancer')
    planet_gen = PlanetGenerator(2021)
    c = 0
    for i in range(1000):
        sl = gen.generate_systems(i)
        planets = planet_gen.generate_planets(sl)
        # print(planets)
        print(sl.string(print_parts=True))
        for p in planets.values():
            if p.colonizable:
                c += 1

    print(c)
