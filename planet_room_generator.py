import numpy.random as random
import json
import os

from rooms import Room
from things import Thing
from custom_json import custom_load


class PlanetRoomGenerator:
    """

    """
    def __init__(self, seed, limit=1):
        self.seed = seed
        with open(os.path.join("Generators", (self.__class__.__name__.lower() + '.json')), 'r') as file:
            self.generator_data = json.load(file)
        with open(os.path.join("Generators", "threats.json"), 'r') as file:
            self.threat_data = json.load(file)
        self.limit = limit

    def generate_landing_spot(self, game, solarsystem, planet):
        i = 0
        for i, p_key in enumerate(solarsystem.contents.keys()):
            p = solarsystem.contents[p_key]['obj']
            if p == planet:
                break
        seed = self.seed + solarsystem.name_seed + i
        game.rooms = dict()
        game.rooms['t0p0'] = self.__generate_room('t0p0', seed, planet, solarsystem)
        self.generate_rooms(game, solarsystem, planet)
        game.refresh_things()

    def generate_rooms(self, game, solarsystem, planet):
        i = 0
        for i, p_key in enumerate(solarsystem.contents.keys()):
            p = solarsystem.contents[p_key]['obj']
            if p == planet:
                break
        seed = self.seed + solarsystem.name_seed + i
        current_room = game.rooms[game.game_state['current room']]
        current_chapter = game.chapters[game.game_state['current chapter']]
        rooms_dir, new_rooms, old_rooms = self._adj_room_coordinates(current_room, game.rooms)

        current_room.directions = rooms_dir
        for new_room_key in new_rooms:
            new_room = self.__generate_room(new_room_key, seed, planet, solarsystem)
            game.rooms[new_room_key] = new_room
            current_chapter.map_files.append(new_room_key)

        for old_room_key in old_rooms:
            if old_room_key == game.game_state['current room']:
                continue
            del game.rooms[old_room_key]
            try:
                current_chapter.map_files.remove(old_room_key)
            except ValueError:
                pass
        game.refresh_things()

    def __generate_room(self, room_key, seed, planet, solarsystem):
        t = int(room_key[1:self.limit+1])
        p = int(room_key[2+self.limit:])
        seed *= (t+1)
        seed /= (p+1)
        seed += ((t+1)*(p+1))
        seed = int(seed)
        random.seed(seed)

        room_types = []
        for elem in planet.entity_state['features']['geology']:
            room_types.append(elem)
        if planet.lifeforms in {"Animal Life", "Advanced Life"}:
            room_types.append("forest")
        if planet.lifeforms == "Former Advanced Life":
            room_types.append("abandoned city")
        if planet.lifeforms == "Advanced Life":
            room_types.append("city")

        new_room = Room(key=room_key, display_name=room_key, reference_noun=room_key)
        new_room.entity_state['room type'] = random.choice(room_types)
        new_room.display_name = new_room.entity_state['room type']
        self.generate_description(new_room, seed, planet, solarsystem)
        self.__load_threat_objects(planet, new_room)
        colony = Thing(key='colony', reference_noun='colony', display_name='colony',
                       description='A Union Colony has not yet been set up on this planet.',
                       as_dirobj={'Setup': True},
                       action_description={"Setup":
                                           "Thus, you begin the construction of your colony on planet {planet}."})
        new_room += colony
        return new_room

    def generate_description(self, room, seed, planet, solarsystem):
        room_type = room.entity_state['room type']

        room_key = room.key
        t = int(room_key[1:1 + self.limit])
        p = int(room_key[2 + self.limit:])
        description = f"Latitude: {p}, Longitude: {t}.\n"

        random.seed(seed)
        description += self.generator_data[room_type]['description']
        template = random.choice(self.generator_data[room_type]['templates'])

        clouds = ''
        rings = ''
        atmosphere = ''
        radiation = ''
        temperature = ''

        if planet.atmosphere_type == "Cloudy Atmosphere":
            clouds = 'The sky is barely visible through the clouds covering the entire planet.\n'
        if planet.entity_state['features']['rings'] == "extensive":
            rings = f"The view of {planet.display_name}'s rings is breathtaking.\n"
        if planet.atmosphere_type == "No Atmosphere":
            atmosphere = "Your pressure sensors record almost no atmosphere. " \
                         "You wouldn't be able to breath without a suit on."
        if planet.atmosphere_type == "Thick Atmosphere":
            atmosphere = 'There is no need for a suit here, maybe just some oxygen tanks for extra intake.'
        if planet.atmosphere_type == "Cloudy Atmosphere":
            atmosphere = 'There is no need for a suit here, maybe just some oxygen tanks for extra intake.'
        if planet.atmosphere_type == "Acid Atmosphere":
            atmosphere = 'Something corrosive in the air is slowly eating away on your equipment.'
        if solarsystem.habitable:
            radiation = 'Radiation levels are tolerable.'
        if not solarsystem.habitable:
            radiation = "Radiation levels are really high, it's almost too dangerous to be walking on the surface."
        if planet.temperature == "Warm":
            temperature = 'The temperature is hot enough to make you uncomfortable, ' \
                          'but you reckon you can withstand it.'
        if planet.temperature == "Temperate":
            temperature = "The temperature is close enough to a mild spring day on Earth."
        if planet.temperature == "Cold":
            temperature = "The temperature hovers just above zero, but you're used to the cold."
        if planet.temperature == "Frozen":
            temperature = "The temperature is constantly below zero. Nothing but extremophiles could survive here."
        if planet.temperature == "Icy":
            temperature = "Even with the cutting edge anti-freeze tech of your suit, the cold is unbearable.\n" \
                          "There are small ponds of liquid methane around you."

        template = template.format(num_stars=len(solarsystem.star_names),
                                   star_plural='' if len(solarsystem.star_names) == 1 else 's',
                                   clouds=clouds, sky_color=planet.entity_state['features']['sky color'],
                                   num_satellites=planet.num_satellites,
                                   satellite_plural='' if planet.num_satellites == 1 else 's',
                                   rings=rings, atmosphere=atmosphere, radiation=radiation, temperature=temperature)

        room.examine_description = description + template
        room.description = description
        room.audible_description = self.generator_data[room_type]['audible']

    def __load_threat_objects(self, planet, room):
        clues = custom_load(os.path.join("Generators", "clues.json"))
        threats = planet.entity_state['features']['threats']
        for threat in threats.keys():
            if threats[threat]:
                # Place clue
                if self.threat_data[threat]['clues']:
                    place_clue = random.choice([True, False], p=[0.8, 0.2])
                    if place_clue:
                        clue_key = random.choice(self.threat_data[threat]['clues'])
                        clue = clues[clue_key]
                        room += clue

    def generate_things(self):
        pass

    def _adj_room_coordinates(self, room, rooms_dict):
        room_key = room.key
        t_coord = int(room_key[1:1+self.limit])
        p_coord = int(room_key[2+self.limit:])

        directions = dict()
        adj_rooms = []

        t, p = self._coordinates(t_coord, p_coord, 0, 1)
        new_room_key = f"t{t}p{p}"
        adj_rooms.append(new_room_key)
        directions['North'] = {"room": new_room_key, "desc": f"Latitude: {p}, Longitude: {t}."}

        t, p = self._coordinates(t_coord, p_coord, -1, 1)
        new_room_key = f"t{t}p{p}"
        adj_rooms.append(new_room_key)
        directions['Northeast'] = {"room": new_room_key, "desc": f"Latitude: {p}, Longitude: {t}."}

        t, p = self._coordinates(t_coord, p_coord, 1, 1)
        new_room_key = f"t{t}p{p}"
        adj_rooms.append(new_room_key)
        directions['Northwest'] = {"room": new_room_key, "desc": f"Latitude: {p}, Longitude: {t}."}

        t, p = self._coordinates(t_coord, p_coord, -1, 0)
        new_room_key = f"t{t}p{p}"
        adj_rooms.append(new_room_key)
        directions['East'] = {"room": new_room_key, "desc": f"Latitude: {p}, Longitude: {t}."}

        t, p = self._coordinates(t_coord, p_coord, 1, 0)
        new_room_key = f"t{t}p{p}"
        adj_rooms.append(new_room_key)
        directions['West'] = {"room": new_room_key, "desc": f"Latitude: {p}, Longitude: {t}."}

        t, p = self._coordinates(t_coord, p_coord, 0, -1)
        new_room_key = f"t{t}p{p}"
        adj_rooms.append(new_room_key)
        directions['South'] = {"room": new_room_key, "desc": f"Latitude: {p}, Longitude: {t}."}

        t, p = self._coordinates(t_coord, p_coord, -1, -1)
        new_room_key = f"t{t}p{p}"
        adj_rooms.append(new_room_key)
        directions['Southeast'] = {"room": new_room_key, "desc": f"Latitude: {p}, Longitude: {t}."}

        t, p = self._coordinates(t_coord, p_coord, 1, -1)
        new_room_key = f"t{t}p{p}"
        adj_rooms.append(new_room_key)
        directions['Southwest'] = {"room": new_room_key, "desc": f"Latitude: {p}, Longitude: {t}."}

        new_rooms = []
        old_rooms = []
        for room_key in rooms_dict.keys():
            if room_key not in adj_rooms:
                old_rooms.append(room_key)

        for room_key in adj_rooms:
            if room_key not in rooms_dict.keys():
                new_rooms.append(room_key)

        return directions, new_rooms, old_rooms

    def _coordinates(self, theta, phi, dtheta, dphi):
        new_theta = theta + dtheta
        new_phi = phi + dphi

        if new_phi < 0:
            new_phi += 10**self.limit

        if new_theta < 0:
            new_theta += 10**self.limit

        new_theta = new_theta % (10**self.limit)
        new_phi = new_phi % (10**self.limit)

        return new_theta, new_phi




