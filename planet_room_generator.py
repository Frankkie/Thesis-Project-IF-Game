import numpy.random as random
import json
import os

from rooms import Room
from things import Thing


class PlanetRoomGenerator:
    """

    """
    def __init__(self, seed, limit=1):
        self.seed = seed
        with open(os.path.join("Generators", (self.__class__.__name__.lower() + '.json')), 'r') as file:
            self.generator_data = json.load(file)
        self.limit = limit

    def generate_landing_spot(self, game, solarsystem, planet):
        i = 0
        for i, p_key in enumerate(solarsystem.contents.keys()):
            p = solarsystem.contents[p_key]['obj']
            if p == planet:
                break
        seed = self.seed + solarsystem.name_seed + i
        game.rooms['t0p0'] = self.generate_room('t0p0', seed)
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
            new_room = self.generate_room(new_room_key, seed)
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

    def generate_room(self, room_key, seed):
        t = int(room_key[1:self.limit+1])
        p = int(room_key[2+self.limit:])
        seed += (t*(10**self.limit)) + p
        new_room = Room(key=room_key, display_name=room_key, reference_noun=room_key)
        new_room.description = self.generate_description(seed)
        colony = Thing(key='colony', reference_noun='colony', display_name='colony',
                       description='A Union Colony has not yet been set up on this planet.',
                       as_dirobj={'Setup': True},
                       action_description={"Setup":
                                           "Thus, you begin the construction of your colony on planet {planet}."})
        new_room += colony
        return new_room

    def generate_description(self, seed):
        return ""

    def generate_threat(self):
        pass

    def generate_things(self):
        pass

    def generate_topics(self):
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




