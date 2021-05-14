"""
    The Entity Class is the parent of the classes:
        Thing
        Room
        Actor
"""
from errors import *
import json


class Entity:
    def __init__(self, key, reference_noun, display_name, description=None,
                 as_indobj=None, as_dirobj=None, container=None, contents=None, plural=False,
                 examine_description=None, audible_description=None, action_description=None, entity_state=None):
        """
        This is the parent class of all Entities (Things, Rooms, Actors).

        Args:
            :param key: str
                This is the name of the object when referenced internally by the game.
            :param reference_noun: str
                This is the noun by which the object is referenced by the player. Must be a single word.
            :param display_name: str
                This is the string by which the game displays the object.
            :param description:
                default="", this is the string by which the object is described by the look method.
            :param container:
                default=None, this is key of the container Entity of the object.
            :param contents:
                default=None, dictionary. The components of this object: {key: {obj: Entity Instance, tags: []}}
            :param as_indobj: A dictionary of the qualifier types that this entity instance can appear
                               with as an indirect object.
            :param as_dirobj: A dictionary of the verbs that this entity instance can appear with as
                              a direct object.
            :param plural: False if the object is a single entity, True if it is multiple entities.
            :param examine_description: default=None, this is the description of the object that is triggered
                                        when the Look command is given to it.
            :param audible_description: default=None, this is the auditory description of the object, triggered
                                        by the Listen command.
            :param action_description: default=None, this is a dictionary of the descriptions of various commands.
                                       {verb name: description}
        """

        self.key = key
        self.reference_noun = reference_noun
        self.display_name = display_name
        self.description = description
        self.container = container
        if not contents:
            self.contents = {}
        else:
            self.contents = contents

        with open("Grammar/qualifiers.json", "r") as file:
            qualifier_types = json.load(file)
        file.close()
        for q in qualifier_types.keys():
            qualifier_types[q] = False
        if not as_indobj:
            self.as_indobj = qualifier_types
        else:
            self.as_indobj = {**qualifier_types, **as_indobj}

        with open("Grammar/verbs.json", "r") as file:
            verbs = json.load(file)
        file.close()
        for q in verbs.keys():
            verbs[q] = False

        if not as_dirobj:
            self.as_dirobj = verbs
        else:
            self.as_dirobj = {**verbs, **as_dirobj}

        if not action_description:
            self.action_description = verbs
        else:
            self.action_description = {**verbs, **action_description}

        self.plural = plural
        self.examine_description = examine_description
        self.audible_description = audible_description
        if not entity_state:
            entity_state = {}
        self.entity_state = entity_state

    def __str__(self):
        try:
            seen = self.entity_state["Seen"]
        except KeyError:
            seen = False
        if self.examine_description and not seen:
            printable = f"The {self.display_name}: " + self.examine_description
        elif self.description:
            printable = f"The {self.display_name}: " + self.description
        else:
            printable = f"There is nothing interesting about the {self.display_name}."
        printable += '\n'

        return printable

    def __iadd__(self, other):
        """
        This method adds another object descended from Entity to this object's self.parts.
        It also updates the other.container to self.key.
        :param other: dictionary, other['obj'] should be an Entity instance,
                                  other['tags'] should be a list of tags (verb and qualifier names).
        :return: The object itself.
        """
        if isinstance(other, dict):
            if isinstance(other['obj'], Entity):
                obj = other['obj']
                obj.container = self.key
                tags = other['tags']
            else:
                raise TypeError
        elif isinstance(other, Entity):
            obj = other
            obj.container = self.key
            tags = ["Inventory", "Look"]
        else:
            raise TypeError

        self.contents[obj.key] = {"obj": obj, "tags": tags}
        return self

    def __isub__(self, other):
        """
        This method removes another object descended from Entity from this object's self.parts.
        It also updates the other.container to self.key.
        :param other: should be an Entity Instance.
        :return: The object itself.
        """
        if isinstance(other, Entity):
            if other.key in self.contents.keys():
                del self.contents[other.key]
                other.container = None
            else:
                raise ActionError("ObjectNotHereError", obj=other.display_name, container=self.display_name)
        else:
            raise TypeError
        return self

    def to_json(self):
        """
        Convert the instance of this class to a serializable object.

        :return: Dictionary
            A dictionary of the object's attributes, containing the key '_class_'.

        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = self.__class__.__name__
        return obj_dict

    def get_contents(self):
        contents = {}
        for key in self.contents.keys():
            if isinstance(self.contents[key], dict):
                contents[key] = self.contents[key]['obj']
                obj_contents = self.contents[key]['obj'].get_contents()
                contents = {**contents, **obj_contents}
        return contents

    def on_dir_object(self, **kwargs):
        verb = kwargs['verb']
        verb_name = verb.name.lower()
        method_name = "_on_" + verb_name
        try:
            method = getattr(self, method_name)
        except AttributeError:
            raise ActionError("ActionNotInObjectError", verb=verb_name, obj=self.display_name)

        result = method(**kwargs)
        return result

    def _on_look(self, **kwargs):
        game = kwargs['game']
        if self.contents:
            for obj in self.contents.keys():
                if "Look" in self.contents[obj]['tags']:
                    game.things[obj] = self.contents[obj]['obj']
                    self.contents[obj]['obj'].is_known = True

        try:
            descr = self.string()
        except AttributeError:
            descr = str(self)

        self.entity_state["Seen"] = True
        return descr

    def _on_listen(self, **kwargs):
        game = kwargs['game']
        self.entity_state["Listened"] = True
        if self.contents:
            for obj in self.contents.keys():
                if "Listen" in self.contents[obj]['tags']:
                    game.things[obj] = self.contents[obj]['obj']
                    self.contents[obj]['obj'].is_known = True
        if self.audible_description:
            return self.audible_description
        else:
            return f"You don't hear anything interesting around the {self.display_name}."

    def _on_take(self, **kwargs):
        actor = kwargs['actor']
        game = kwargs['game']
        room_key = actor.container
        room = game.rooms[room_key]
        container_key = self.container
        if container_key == room_key:
            room -= self
        else:
            container_object = game.things[container_key]
            container_object -= self

        actor += {"obj": self, "tags": ["Inventory", "Look"]}
        if self.action_description["Take"]:
            return self.action_description["Take"]
        else:
            v = "is"
            if self.plural:
                v = "are"
            p = "in your hands"
            if actor.key != "I":
                p = actor.key + "'s"
            return f"The {self.display_name} {v} now {p}."

    def _on_drop(self, **kwargs):
        game = kwargs['game']
        actor = kwargs['actor']
        actor -= self
        room_key = actor.container
        room = game.rooms[room_key]
        room += {"obj": self, "tags": ["Inventory", "Look"]}

        if self.action_description["Drop"]:
            return self.action_description["Drop"]
        else:
            return f"You leave the {self.display_name} in the {room.display_name}."

    def _on_put(self, **kwargs):
        ind_object = kwargs['indirect']
        qualifier = kwargs['qualifier']
        actor = kwargs['actor']
        actor -= self
        ind_object += {'obj': self, 'tags': ['Look', 'Inventory', qualifier]}
        return f'You put the {self.display_name} {qualifier.lower()} the {ind_object.display_name}.'

    def _on_read(self, **kwargs):
        self.entity_state["Read"] = True
        if self.action_description["Read"]:
            return self.action_description["Read"]
        else:
            return f"There's nothing to read on the {self.display_name}."

    def _on_use(self, **kwargs):
        self.entity_state["Used"] = True
        result = self.action_description["Use"]
        indirect = kwargs["indirect"]
        if indirect:
            indirect.entity_state["On Used " + self.key] = True
            result += "\n"
            result += indirect.action_description["On Use " + self.key]
        return result

    def _on_push(self, **kwargs):
        self.entity_state["Pushed"] = True

        if self.action_description["Push"]:
            return self.action_description["Push"]
        else:
            return f"You push the {self.display_name}."

    def _on_close(self, **kwargs):
        descr = ''
        if self.action_description["Open"]:
            descr += self.action_description["Open"]
        else:
            descr += f"You close the {self.display_name}."
        for content in self.contents.values():
            if 'In' in content["tags"]:
                content['obj'].is_known = False

        self.entity_state['Open'] = False
        return descr

    def _on_open(self, **kwargs):
        descr = ''
        if self.action_description["Open"]:
            descr += self.action_description["Open"]
        else:
            descr += f"You open the {self.display_name}."

        descr += '\n'
        for content in self.contents.values():
            if 'In' in content["tags"]:
                descr += f"- {content['obj'].string(print_parts=False)}\n"
                content['obj'].is_known = True

        self.entity_state['Open'] = True
        return descr

    def _on_leave(self, **kwargs):
        pass

    def _on_setup(self, **kwargs):
        pass

    def _on_swerveoff(self, **kwargs):
        pass

    def _on_enter(self, **kwargs):
        pass

    def _on_landon(self, **kwargs):
        pass

    def _on_send(self, **kwargs):
        pass

