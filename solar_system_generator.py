import numpy as np

from name_generator import NameGenerator
from space_things import SolarSystem


class SolarSystemGenerator:
    """

    """
    def __init__(self, seed, constellation):
        self.seed = seed
        self.constellation = constellation
        self.star_name_gen = NameGenerator(self.seed, 'star_name_grammar.cfg', prefix=self.constellation)
        self.generated = set()
        self.star_numbers = [1, 2, 3, 4, 5]
        self.star_number_weights = [0.6, 0.2, 0.1, 0.07, 0.03]
        self.star_types = ['Blue Giant', 'Red Giant', 'Yellow Dwarf', 'Red Dwarf',
                           'Neutron Star', 'Black Hole', 'Brown Dwarf', 'White Dwarf']
        self.star_type_weights = [0.05, 0.05, 0.5, 0.3, 0.01, 0.01, 0.06, 0.02]
        self.planet_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.planet_numbers_weights = [0.25, 0.05, 0.05, 0.1, 0.15, 0.2, 0.1, 0.05, 0.05]

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
            habitable = True
            for t in star_types:
                if t not in ['Yellow Dwarf', 'Red Dwarf', 'Black Hole', 'Brown Dwarf']:
                    habitable = False
                    break

        num_planets = np.random.choice(self.planet_numbers, p=self.planet_numbers_weights)

        sl = SolarSystem(key=name, reference_noun='system', display_name=name, reference_adjectives=['solar', name],
                         star_names=star_names, star_types=star_types, habitable=habitable, num_planets=num_planets)

        return sl

    def hash_system_name(self, name):
        system_seed = 1
        for c in list(name):
            system_seed *= (ord(c) + 1)
        system_seed /= 10000
        system_seed = int(system_seed) % (10 ** 8)
        if system_seed in self.generated:
            return self.hash_system_name(name+'a')
        self.generated.add(system_seed)
        return system_seed


class PlanetGenerator:
    """

    """
    def __init__(self, seed):
        self.seed = seed
        self.star_name_gen = NameGenerator(self.seed, 'planet_name_grammar.cfg')
        self.generated = set()

    def generate_planets(self, system):
        pass


if __name__ == '__main__':
    gen = SolarSystemGenerator(1998, 'Cancer')

    for i in range(1000):
        print(gen.generate_systems(i).string(print_parts=False))

