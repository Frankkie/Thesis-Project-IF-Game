from entities import Entity


class Actor(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        This is the parent class of all Actors.
        
        """
