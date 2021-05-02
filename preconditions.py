from errors import PreconditionsError


class ActionPreconditions:
    def __init__(self, syntax, actor, verb, obj, qualifier, ind_obj):
        self.syntax = syntax
        self.actor = actor
        self.verb = verb
        self.obj = obj
        self.qualifier = qualifier
        self.ind_obj = ind_obj

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
        return True