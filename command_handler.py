from errors import CheckCommandError, PreconditionsError, ActionError, DialogError
from preconditions import ActionPreconditions


class CommandHandler:
    def __init__(self, game):
        self.command = None
        self.syntax = ""
        self.game = game

    def run_command(self, sentence, syntax):
        self.command = []
        self.syntax = syntax

        objects = sentence["Object"]
        ind_objects = sentence["Indirect"]
        actor = sentence["Actor"]
        verb = sentence["Verb"]
        qualifier = sentence["Qualifier"]

        many_objects = False
        many_ind_objects = False

        # Unfold the direct and indirect objects of the command into separate sentences.
        if objects:
            if len(objects) > 1:
                many_objects = True
            else:
                objects = objects[0]
            if ind_objects:
                if len(ind_objects) > 1:
                    many_ind_objects = True
                else:
                    ind_objects = ind_objects[0]
            if many_ind_objects and many_objects:
                raise CheckCommandError("ManyDirIndObjectsError")
            if many_objects:
                self.command = [{"Actor": actor, "Verb": verb, "Object": obj,
                                 "Qualifier": qualifier, "Indirect": ind_objects} for obj in objects]
            elif many_ind_objects:
                self.command = [{"Actor": actor, "Verb": verb, "Object": objects,
                                 "Qualifier": qualifier, "Indirect": ind} for ind in ind_objects]
            else:
                self.command = [{"Actor": actor, "Verb": verb, "Object": objects,
                                 "Qualifier": qualifier, "Indirect": ind_objects}]
        else:
            self.command = [{"Actor": actor, "Verb": verb, "Object": objects,
                             "Qualifier": qualifier, "Indirect": ind_objects}]

        # If this command is directed to the Player Character
        if actor == self.game.actors["I"]:
            for sentence in self.command:
                try:
                    self.pc_command(sentence, syntax, many_ind_objects)
                except (CheckCommandError, PreconditionsError, ActionError, DialogError) as error:
                    raise error

        # If this command is directed to an NPC
        else:
            for sentence in self.command:
                try:
                    self.npc_command(sentence, syntax, many_ind_objects)
                except (CheckCommandError, PreconditionsError, ActionError, DialogError) as error:
                    raise error

    def pc_command(self, sentence, syntax, many_ind_objects):
        # Prepare for action
        try:
            self.prepare_execution(sentence, syntax, many_ind_objects)
        except (CheckCommandError, PreconditionsError, ActionError, DialogError) as error:
            raise error

        try:
            self.action_execution(sentence, syntax)
        except (ActionError, DialogError) as error:
            raise error

    def npc_command(self, sentence, syntax, many_ind_objects):
        # Check npc commandability
        actor = sentence["Actor"]
        verb_name = sentence["Verb"].name
        if not actor.on_command[verb_name]:
            raise CheckCommandError("NPCNotCommandableError", actor=actor.display_name)
        if actor.container != self.game.game_state["current room"] and verb_name not in ["Go"]:
            npc_room_name = self.game.rooms[actor.container].display_name
            pc_room_key = self.game.game_state["current room"]
            pc_room_name = self.game.rooms[pc_room_key].display_name
            raise CheckCommandError("NPCNotInCurrentRoomError", actor=actor.display_name,
                                    pc_room=pc_room_name, npc_room=npc_room_name)

        # Prepare for action
        try:
            self.prepare_execution(sentence, syntax, many_ind_objects)
        except (CheckCommandError, PreconditionsError, ActionError, DialogError) as error:
            raise error

        try:
            self.action_execution(sentence, syntax)
        except (ActionError, DialogError) as error:
            raise error

    def prepare_execution(self, sentence, syntax, many_ind_objects):
        """
        This method determines whether the command given by the player can be executed.
        If the action is allowed, the method returns True.
        If not, the method returns an error code (string).
        :param sentence: Dictionary with the command parts.
        :param syntax: The syntax of the command.
        :return: True if the action is allowed, an error code (str) if the action is not allowed.
        """

        actor = sentence["Actor"]
        verb = sentence["Verb"]
        obj = sentence["Object"]
        qualifier = sentence["Qualifier"]
        ind_obj = sentence["Indirect"]

        try:
            self.__check_actor(actor, verb)
        except CheckCommandError as error:
            raise error

        if qualifier:
            try:
                self.__check_qualifier(actor, verb, qualifier, ind_obj, many_ind_objects)
            except CheckCommandError as error:
                raise error

        if obj:
            try:
                self.__check_object(verb, obj)
            except CheckCommandError as error:
                raise error

        if verb.name in ["Ask"]:
            try:
                self.__check_topic(ind_obj, obj)
            except CheckCommandError as error:
                raise error

        try:
            self.__check_preconditions(syntax, actor, verb, obj, qualifier, ind_obj)
        except PreconditionsError as error:
            raise error

        self.game.saver.save_to_temp()

        return True

    def action_execution(self, sentence, syntax):
        actor = sentence["Actor"]
        verb = sentence["Verb"]
        obj = sentence["Object"]
        qualifier = sentence["Qualifier"]
        ind_obj = sentence["Indirect"]
        result = None

        if verb.name in ["Ask"]:
            try:
                result = self.__dialog(obj, ind_obj)
                self.game.display.queue(result, "Dialog")
                return
            except DialogError as error:
                raise error

        else:
            for a in self.game.actors.values():
                if a.active_convonode != 'ready':
                    a.active_convonode = 'ready'
                    try:
                        res = self.game.dialogevents["goodbye_general"].trigger(self.game)
                        self.game.display.queue(res, "Dialog")
                    except KeyError:
                        pass

        if syntax == "":
            try:
                result = self.__action_(actor, verb)
            except ActionError as error:
                raise error
        elif syntax == "Q":
            try:
                result = self.__action_q(actor, verb, qualifier)
            except ActionError as error:
                raise error
        elif syntax == "O":
            try:
                result = self.__action_o(actor, verb, obj)
            except ActionError as error:
                raise error
        elif syntax == "OQI":
            try:
                result = self.__action_oqi(actor, verb, obj, qualifier, ind_obj)
            except ActionError as error:
                raise error

        self.game.display.queue(result, 'AfterAction')

    def __check_actor(self, actor, verb):
        verb_name = verb.name
        if actor.abilities[verb_name]:
            return
        else:
            raise CheckCommandError("ActorNotAbleError", actor=actor.display_name.capitalize())

    def __check_qualifier(self, actor, verb, qualifier, ind_object, many_ind_objects):
        if ind_object:
            if verb.name in ["Use"]:
                if qualifier == "On":
                    return
                else:
                    raise CheckCommandError("VerbQualifierNotValidError", verb=verb.name, qualifier=qualifier)

            if verb.name in ["Ask"]:
                if qualifier == "About":
                    return
                else:
                    raise CheckCommandError("VerbQualifierNotValidError", verb=verb.name, qualifier=qualifier)

            if qualifier in ind_object.as_indobj.keys():
                if ind_object.as_indobj[qualifier]:
                    if many_ind_objects:
                        if qualifier in ["To"]:
                            return
                        else:
                            raise CheckCommandError("ManyIndObjectsError")
                    else:
                        return
                else:
                    raise CheckCommandError("IndObjectQualifierNotValidError", ind_object=ind_object.display_name)
            else:
                raise CheckCommandError("IndObjectQualifierNotValidError", ind_object=ind_object.display_name)
        else:
            if verb.name in ["Go"]:
                actor_room_key = actor.container
                actor_room = self.game.rooms[actor_room_key]
                directions = actor_room.directions.keys()
                if qualifier in directions:
                    return
                else:
                    raise CheckCommandError("DirectionNotValidError", qualifier=qualifier)
            else:
                raise CheckCommandError("VerbQualifierNotValidError", verb=verb.name, qualifier=qualifier)

    def __check_object(self, verb, obj):
        verb_name = verb.name
        if verb_name in obj.as_dirobj.keys():
            if obj.as_dirobj[verb_name]:
                return
            else:
                raise CheckCommandError("ObjectNotAbleError", obj=obj.display_name, verb=verb_name.lower())
        else:
            raise CheckCommandError("ObjectNotAbleError", obj=obj.display_name, verb=verb_name.lower())

    def __check_topic(self, topic, actor_asked):
        # CHECK WITH THE CONVONODE!!!!!!!!!!!!!!!!!!!!!!!
        pass

    def __check_preconditions(self, syntax, actor, verb, obj, qualifier, ind_obj):
        prec = ActionPreconditions(syntax, actor, verb, obj, qualifier, ind_obj)
        try:
            result = prec.check_preconditions()
            del prec
            return result
        except PreconditionsError as error:
            raise error

    def __action_(self, actor, verb):
        return actor, verb

    def __action_q(self, actor, verb, qualifier):
        if verb.name in ["Go"]:
            try:
                result = actor.on_dir_object(verb=verb, actor=actor, game=self.game, qualifier=qualifier.capitalize())
                return result
            except ActionError as error:
                raise error

    def __action_o(self, actor, verb, obj):
        try:
            result = obj.on_dir_object(verb=verb, actor=actor, game=self.game)
            return result
        except ActionError as error:
            raise error

    def __action_oqi(self, actor, verb, obj, qualifier, indirect):
        return actor, verb, obj, qualifier, indirect

    def __dialog(self, actor_asked, topic):
        try:
            result = topic.on_topic(game=self.game, actor=actor_asked)
            return result
        except DialogError as error:
            raise error

