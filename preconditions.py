from errors import PreconditionsError


class ActionPreconditions:
    def __init__(self, syntax, actor, verb, obj, qualifier, ind_obj, game):
        self.syntax = syntax
        self.actor = actor
        self.verb = verb
        self.obj = obj
        self.qualifier = qualifier
        self.ind_obj = ind_obj
        self.game = game

    def check_preconditions(self):
        verb_name = self.verb.name.lower()
        method_name = "_" + verb_name
        try:
            method = getattr(self, method_name)
        except AttributeError:
            return True

        result = method()
        return result

    def _go(self):
        return True

    def _look(self):
        return True

    def _take(self):
        return True

    def _put(self):
        if self.obj.key not in self.actor.contents:
            raise PreconditionsError("TakeObjectError", obj=self.obj.display_name)

        if self.qualifier == 'In':
            try:
                ind_open = self.ind_obj.entity_state['Open']
            except KeyError:
                raise PreconditionsError('IndObjectNotOpen', ind_obj=self.ind_obj.display_name)
            if not ind_open:
                raise PreconditionsError('IndObjectNotOpen', ind_obj=self.ind_obj.display_name)
        return True

    def _use(self):

        if not self.obj.action_description['Use']:
            raise PreconditionsError("UseObjectError", obj=self.obj.display_name)

        if self.ind_obj:
            if "On Use " + self.obj.key not in self.ind_obj.action_description.keys():
                raise PreconditionsError("UseOnObjectError", obj=self.obj.display_name,
                                         ind_obj=self.ind_obj.display_name)
            else:
                return True
        return True

    def _open(self):
        return True

    def _enter(self):
        solarsystem = self.obj
        try:
            entered = solarsystem.entity_state["Entered"]
        except KeyError:
            return True
        if entered:
            raise PreconditionsError("SystemAlreadyEnteredError", system_name=solarsystem.display_name)
        return True

    def _leave(self):
        solarsystem = self.obj
        try:
            planet = self.game.game_state['current planet']
        except KeyError:
            return True
        if planet is not None:
            planet = self.game.things[planet]
            raise PreconditionsError("LeaveLandedError", planet=planet.display_name,
                                     solarsystem=solarsystem.display_name)
        return True

    def _landon(self):
        planet = self.obj
        solarsystem = self.game.things[planet.container]

        try:
            entered = solarsystem.entity_state["Entered"]
        except KeyError:
            raise PreconditionsError("SystemNotEnteredError", action="land on", planet=planet.display_name)

        if entered:
            if planet.planet_type == "Dwarf Planet":
                raise PreconditionsError("DwarfPlanetLandingError")
            return True
        else:
            raise PreconditionsError("SystemNotEnteredError", action="land on", planet=planet.display_name)

    def _send(self):
        if self.obj.key != "drones":
            raise PreconditionsError("NotDronesOnSendError", obj=self.obj.display_name)
        if self.ind_obj.__class__.__name__ != "Planet":
            raise PreconditionsError("SendNotOnPlanetError", ind=self.ind_obj.display_name)
        planet = self.ind_obj
        solarsystem = self.game.things[planet.container]
        try:
            entered = solarsystem.entity_state["Entered"]
        except KeyError:
            raise PreconditionsError("SystemNotEnteredError", action="send drones to", planet=planet.display_name)

        if entered:
            return True
        else:
            raise PreconditionsError("SystemNotEnteredError", action="send drones to", planet=planet.display_name)