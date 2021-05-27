import numpy as np
import json
import os

from name_generator import NameGenerator
from space_things import SolarSystem, Planet
from planet_room_generator import PlanetRoomGenerator


class SolarSystemGenerator:
    """

    """
    def __init__(self, seed, limit=1):
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
        self.descriptions_generator = PlanetDescriptionGenerator(self.seed)
        self.planet_room_generator = PlanetRoomGenerator(self.seed, limit=limit)
        self.landingdescriptiongenerator = LandingDescriptionGenerator(self.seed)
        self.colonydescriptiongenerator = ColonyDescriptionGenerator(self.seed)

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
                         distance=distance, name_seed=name_seed, is_known=True, num_stars=len(star_names))
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
        if 'White Dwarf' in solar_system.star_types \
                or 'Black Hole' in solar_system.star_types \
                or 'Neutron Star' in solar_system.star_types:
            descr += "The remnants of a long gone star are present here, indicating a violent past.\n"
        if 'Blue Giant' not in solar_system.star_types \
                and 'Read Giant' not in solar_system.star_types \
                and 'Yellow Dwarf' not in solar_system.star_types \
                and 'Red Dwarf' not in solar_system.star_types:
            descr += "The system is barely lit by its dim 'stars'."
        solar_system.action_description['On Use telescope'] = descr

    def generate_descriptions(self, solarsystem):
        self.descriptions_generator.generate_descriptions(solarsystem)

    def generate_landing_spot(self, game, solarsystem, planet):
        self.planet_room_generator.generate_landing_spot(game, solarsystem, planet)

    def generate_planet_rooms(self, game, solarsystem, planet):
        self.planet_room_generator.generate_rooms(game=game, planet=planet, solarsystem=solarsystem)

    def generate_landing_description(self, planet):
        return self.landingdescriptiongenerator.generate_description(planet)

    def generate_colony_description(self, planet):
        return self.colonydescriptiongenerator.generate_description(planet)


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
            name = self.star_name_gen.generate_name(system_seed + (i + r) * r)
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
            planet['action_description'] = {'On Send': "Sent drones!",
                                            'On Use telescope': 'Examining this planet further that far away is '
                                                                'impossible.\nYou have to enter its parent system '
                                                                'to take a closer look.',
                                            'Landon': 'You are slowly descending onto {name}.',
                                            'Takeoff': 'You leave {name} behind.'}
            planet = Planet(**planet)
            planets[name] = {'obj': planet, 'tags': ['Planet', 'Look', 'Inventory']}

        system.contents = planets

        return planets


class PlanetDescriptionGenerator:
    def __init__(self, game_seed):
        self.game_seed = game_seed
        with open(os.path.join("Generators", (self.__class__.__name__.lower() + '.json')), 'r') as file:
            self.generator_data = json.load(file)

    def generate_descriptions(self, solarsystem):
        i = 0
        for key in solarsystem.contents:
            planet = solarsystem.contents[key]['obj']
            self.choose_features(planet, self.game_seed + solarsystem.name_seed + i, solarsystem)
            self.generate_threat(planet, solarsystem)
            self.examine_description(planet)
            self.telescope_description(planet)
            self.drones_description(planet, self.game_seed + solarsystem.name_seed + i)
            i += 1

    def choose_features(self, planet, seed, solarsystem):
        features = {}
        np.random.seed(seed)

        features["orbit"] = np.random.choice(self.generator_data["orbit"][planet.temperature])
        num_stars = len(solarsystem.star_names)
        if num_stars > 3:
            features["orbit"] = "elliptical"
        features["rotation"] = np.random.choice(self.generator_data["rotation"][planet.temperature])
        features["rings"] = np.random.choice(self.generator_data['rings'])

        if planet.rocky_planet_type:
            if planet.rocky_planet_type == "Lava Planet":
                features["surface color"] = np.random.choice(self.generator_data["surface color"]["Lava Planet"])
            else:
                features['geology'] = self.generator_data['geology'][planet.water_type]
                features['sky color'] = np.random.choice(self.generator_data['sky color'][planet.atmosphere_type])
                features["surface color"] = np.random.choice(self.generator_data["surface color"][planet.water_type])
        planet.entity_state['features'] = features

    def generate_threat(self, planet, solarsystem):
        threat_types = {'cold threat': False,
                        'water threat': False,
                        'desert threat': False,
                        'elliptical threat': False,
                        'radiation threat': False,
                        'air threat': False,
                        'microbe threat': False,
                        'animal threat': False,
                        'ruins threat': False,
                        'genius threat': False
                        }

        if planet.water_type == 'Ice Planet':
            threat_types['cold threat'] = True
        if planet.water_type == 'Water World':
            threat_types['water threat'] = True
        if planet.water_type == 'Desert Planet':
            threat_types['desert threat'] = True
        if planet.entity_state['features']['orbit'] == 'elliptical':
            threat_types['elliptical threat'] = True
        if planet.entity_state['features']['orbit'] != 'elliptical' and solarsystem.habitable is False:
            threat_types['radiation threat'] = True
        if planet.atmosphere_type == 'No Atmosphere':
            threat_types['air threat'] = True
        if planet.atmosphere_type == 'Acid Atmosphere':
            threat_types['acid threat'] = True
        if planet.lifeforms == 'Primordial Life':
            threat_types['microbe threat'] = True
        if planet.lifeforms == 'Animal Life':
            threat_types['animal threat'] = True
        if planet.lifeforms == 'Former Advanced Life':
            threat_types['ruins threat'] = True
        if planet.lifeforms == 'Advanced Life':
            threat_types['genius threat'] = True

        planet.entity_state['features']['threats'] = threat_types

    def examine_description(self, planet):
        description = self.generator_data["descriptions"][planet.planet_type] + \
                      self.generator_data["descriptions"][planet.entity_state['features']['orbit']]
        planet.examine_description = description

    def telescope_description(self, planet):
        rings = planet.entity_state["features"]["rings"]
        description = f'{self.generator_data["descriptions"][planet.planet_type]}' \
                      f'There {"are" if planet.num_satellites != 1 else "is"} ' \
                      f'{planet.num_satellites} satellite{"s" if planet.num_satellites != 1 else ""} ' \
                      f'orbiting around it.\n{self.generator_data["descriptions"][rings]}' \
                      f'{self.generator_data["descriptions"][planet.entity_state["features"]["orbit"]]}'

        if "surface color" in planet.entity_state['features']:
            surface = planet.entity_state['features']['surface color']
            description += f"{surface.capitalize()} seems to be the color dominating its surface."
        planet.action_description["On Use telescope"] = description

    def drones_description(self, planet, seed):
        np.random.seed(seed)
        drones_destroyed = np.random.choice([True, False], p=[0.2, 0.8])
        if drones_destroyed:
            description = np.random.choice(self.generator_data["descriptions"]["drones destroyed"])

        else:
            rotation = self.generator_data["descriptions"][planet.entity_state["features"]["rotation"]]
            temperature = self.generator_data["descriptions"][planet.temperature]
            description = planet.action_description["On Use telescope"] + "\n"
            description += (rotation + temperature)
            if planet.atmosphere_type == "Cloudy Atmosphere":
                description += "Unfortunately, due to the dense cloud cover of the atmosphere, " \
                               "we were unable to retrieve any extra information about the planet."
            elif planet.atmosphere_type is not None:
                description += self.generator_data["descriptions"][planet.atmosphere_type]
                if planet.water_type is not None:
                    description += np.random.choice(
                        self.generator_data["descriptions"][planet.lifeforms])

        planet.action_description["On Send"] = description


class LandingDescriptionGenerator:
    def __init__(self, seed):
        self.seed = seed
        with open(os.path.join("Generators", (self.__class__.__name__.lower() + '.json')), 'r') as file:
            self.generator_data = json.load(file)

    def generate_description(self, planet):
        if planet.rocky_planet_type is None:
            description = self.generator_data['giant']
        elif planet.rocky_planet_type == 'Lava Planet':
            description = self.generator_data['lava']
        else:
            if planet.atmosphere_type == 'No Atmosphere':
                description = self.generator_data['no atmosphere']
            elif planet.atmosphere_type == 'Cloudy Atmosphere':
                description = self.generator_data['cloudy atmosphere']
            else:
                description = self.generator_data['other']
            description = description.format(name=planet.display_name,
                                             surface_color=planet.entity_state['features']['surface color'],
                                             sky_color=planet.entity_state['features']['sky color'])
        return description


class ColonyDescriptionGenerator:
    def __init__(self, seed):
        self.seed = seed
        with open(os.path.join("Generators", "threats.json"), 'r') as file:
            self.threat_data = json.load(file)

    def generate_description(self, planet):
        description = ""
        for threat in planet.entity_state['features']['threats'].keys():
            if planet.entity_state['features']['threats'][threat] and not planet.colonizable:
                description += self.threat_data[threat]['colony'] + '\n'

        if description == "":
            description = "As the years go by, your colony grows stronger and stronger.\n" \
                          "Here you can see the grandeur and vision of the Union back on Earth. Your people\n" \
                          "are now free to build their Utopia undisturbed, and build they do. This is not the\n" \
                          "end, it is just the beginning. Colony ships leave to find more worlds to colonize\n" \
                          "throughout the galaxy. And you know deep down, that some day, the Earth will be yours again!"

        description = ("All together, in the ways of your ancestors you build your new colony\n" +
                       f"on {planet.display_name}, that you now call home...\n" + description)
        description += '\n'

        return description


def choose_constellation(seed):
    import pandas as pd
    file_path = os.path.join('Generators', 'constellations.csv')
    with open(file_path, 'r') as file:
        constellations = pd.read_csv(file)
    constellations = constellations['Constellation'].to_numpy()
    np.random.seed(seed)
    const = np.random.choice(list(constellations))
    return const
