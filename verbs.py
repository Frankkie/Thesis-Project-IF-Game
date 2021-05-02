"""
    Verb Pattern:
        CV are implied
        O: Direct Object(s)
        Q: Qualifier (adjective, or preposition)
        I: Indirect Object or Prepositional Phrase
"""


class Verb:
    def __init__(self, forms, patterns, name):
        self.forms = forms
        self.patterns = patterns
        self.name = name

    def __str__(self):
        return self.name

    def to_json(self):
        """
            convert the instance of this class to json
        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = "Verb"
        return obj_dict


