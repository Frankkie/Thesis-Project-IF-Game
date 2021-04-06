"""
    Verb Pattern:
        CV are implied
        O: Direct Object(s)
        Q: Qualifier (adjective, or preposition)
        I: Indirect Object or Prepositional Phrase
"""


class Verb:
    def __init__(self, forms, pattern):
        self.name = forms[0] + " | " + pattern
        self.forms = forms
        self.pattern = pattern

    def match(self, form, pattern):
        if form in self.forms:
            if pattern == self.pattern:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return self.name

    def to_json(self):
        """
            convert the instance of this class to json
        """
        obj_dict = self.__dict__
        del obj_dict["name"]
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
