import game
from entities import Entity
from custom_json import custom_dump


class Actor(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, plural=False)
        """
        This is the parent class of all Actors.
        
        """
