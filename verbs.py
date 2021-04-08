"""
    Verb Pattern:
        CV are implied
        O: Direct Object(s)
        Q: Qualifier (adjective, or preposition)
        I: Indirect Object or Prepositional Phrase
"""


class Verb:
    def __init__(self, forms, patterns):
        self.forms = forms
        self.patterns = patterns

    def __str__(self):
        return self.forms[0]

    def to_json(self):
        """
            convert the instance of this class to json
        """
        obj_dict = self.__dict__
        obj_dict["_class_"] = "Verb"
        return obj_dict


if __name__ == "__main__":
    pass
    """import custom_json

    v = Verb(["take", "takes", "took"], "O")
    VERBS = {v.name: v}

    with open("verbs.json", "w") as file:
        print(isinstance(v, Verb))
        custom_json.custom_dump(v, file)"""
