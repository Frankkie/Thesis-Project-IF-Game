""" This file defines the exception classes for the game. """


class Error(Exception):
    def __init__(self, error_type):
        self.error_type = error_type
        super().__init__("")

    def error_message(self):
        """
        This function prints an error message.
        :return: String, error message
        """
        return self.error_type

    def __str__(self):
        message = self.error_message()
        return message


class ParserError(Error):
    def __init__(self, error_type):
        super().__init__(error_type)

    def error_message(self):
        """
        This function prints an error message.
        :return: String, error message
        """
        if self.error_type == "GrammarError":
            return "I could not understand your command."
        if self.error_type == "VerbError":
            return "I could not understand this verb."
        if self.error_type == "SyntaxError":
            return "This is the incorrect syntax for this verb."


class NPParserError(Error):
    def __init__(self, error_type):
        super().__init__(error_type)

    def error_message(self):
        """
        This function prints an error message.
        :return: String, error message
        """
        if self.error_type == "EntityError":
            return "This object is not here."
        else:
            return self.error_type


class CheckCommandError(Error):
    def __init__(self, error_type, **kwargs):
        super().__init__(error_type)
        self.kwargs = kwargs

    def error_message(self):
        if self.error_type == "ManyDirIndObjectsError":
            return "You cannot have many Direct & Indirect Objects in the same command."
        if self.error_type == "NPCNotCommandableError":
            return f"{self.kwargs['actor']} does not obey to this order."
        if self.error_type == "ActorNotAbleError":
            return f"{self.kwargs['actor']} cannot perform this command."
        if self.error_type == "DirectionNotValidError":
            return f"You can't go {self.kwargs['qualifier']}."
        if self.error_type == "IndObjectQualifierNotValidError":
            return f"The {self.kwargs['ind_object']} cannot be used in this way."
        if self.error_type == "VerbQualifierNotValidError":
            return f"You cannot use {self.kwargs['qualifier']} as a qualifier with {self.kwargs['verb']}."
        if self.error_type == "ManyIndObjectsError":
            return "You cannot do this to multiple objects."
        if self.error_type == "ObjectNotAbleError":
            return f"You cannot {self.kwargs['verb']} the {self.kwargs['obj']}."
        if self.error_type == "NPCNotInCurrentRoomError":
            return f"{self.kwargs['actor']} is not in the {self.kwargs['pc_room']} with you.\n" \
                   f"You should direct {self.kwargs['actor']} to return from the {self.kwargs['npc_room']} to fulfill" \
                   f" your command."
        if self.error_type == "UndoError":
            return 'You cannot undo twice in a row!'
        else:
            return self.error_type


class PreconditionsError(Error):
    def __init__(self, error_type, **kwargs):
        super().__init__(error_type)
        self.kwargs = kwargs

    def error_message(self):
        if self.error_type == "TakeObjectError":
            return f"You have to take the {self.kwargs['obj']} before doing this."
        if self.error_type == "ActionNotInObjectError":
            return f"The {self.kwargs['obj']} does not have the method {self.kwargs['verb']}."
        if self.error_type == "UseOnObjectError":
            return f"You cannot use the {self.kwargs['obj']} on the {self.kwargs['ind_obj']}."
        if self.error_type == 'IndObjectNotOpen':
            return f'You have to open {self.kwargs["ind_obj"]} first, before you put something in it.'
        if self.error_type == "UseObjectError":
            return f"There is no particular use for the {self.kwargs['obj']}."
        if self.error_type == "SystemNotEnteredError":
            return f"You have to enter the solar system before you {self.kwargs['action']} {self.kwargs['planet']}."
        if self.error_type == "NotDronesOnSendError":
            return f"You cannot send the {self.kwargs['obj']} to a planet."
        if self.error_type == "SendNotOnPlanetError":
            return f"You cannot send drones to a {self.kwargs['ind']}."
        if self.error_type == "DwarfPlanetLandingError":
            return "Due to the low gravity of dwarf planets, it's impossible to safely land on them."
        if self.error_type == "SystemAlreadyEnteredError":
            return f"You are already in the {self.kwargs['system_name']} system."
        if self.error_type == "LeaveLandedError":
            return f'You have to take off of {self.kwargs["planet"]}, ' \
                   f'before you leave the {self.kwargs["solarsystem"]} system.'
        if self.error_type == "NotInBridgeError":
            return f"You have to be in the Spaceship's bridge to {self.kwargs['action']}."
        if self.error_type == "AlreadyLandedError":
            return f"You are already landed on {self.kwargs['planet']}. Take off if you want to visit another planet."
        if self.error_type == "NotOnAPlanetError":
            return "You have to be on a planet to take off."
        if self.error_type == "NotInLandingSpotError":
            return "You have to return to your landing spot (0 Latitude, 0 Longitude) to take off."
        else:
            return self.error_type


class ActionError(Error):
    def __init__(self, error_type, **kwargs):
        super().__init__(error_type)
        self.kwargs = kwargs

    def error_message(self):
        if self.error_type == "ActionNotInObjectError":
            return f"The {self.kwargs['obj']} does not have the method {self.kwargs['verb']}."
        if self.error_type == "ObjectNotHereError":
            return f"The {self.kwargs['obj']} is not in the {self.kwargs['container']}."
        if self.error_type == 'DoorClosedError':
            return f"You have to open the {self.kwargs['door']} before you go {self.kwargs['direction']}."
        else:
            return self.error_type


class DialogError(Error):
    def __init__(self, error_type, **kwargs):
        super().__init__(error_type)
        self.kwargs = kwargs
        self.default_responses = [
            "'You can't expect me to talk about this right now!'",
            "'What a bizarre thing to ask me about!'",
            "'I am not going to entertain this question.'"
        ]

    def error_message(self):
        if self.error_type == "TopicError":
            import random
            return random.choice(self.default_responses)
        if self.error_type == "NoEventForTopic":
            actor = self.kwargs['actor']
            return f"{actor} stays silent."
        if self.error_type == "ConvoNodeNotFound":
            return f'Conversation node {self.kwargs["convonode"]} not found!'
        else:
            return self.error_type


class UndoCommand(Error):
    def __init__(self, error_type):
        super().__init__(error_type)

