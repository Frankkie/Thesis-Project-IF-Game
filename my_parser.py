import nltk
from nltk import tokenize as tok
import string
from custom_json import custom_load


class Parser:
    def __init__(self, actors, verbs):
        self.parser = nltk.ChartParser(nltk.data.load('file:grammar.cfg'))
        self.game_actors = actors
        self.game_verbs = verbs
        self.sent_separators = ('.', '?', '!', ',', 'then', ';')
        self.text = None
        self.current_actors = None
        self.words = None
        self.pos = []
        self.trees = []
        self.parts = []

    def run_parser(self, text):
        self.text = text
        self.text = self.preparse()
        self.words = self.tokenize()
        self.pos = []
        self.trees = []
        self.parts = []
        print(self.words)
        for sentence in self.words:
            sent_pos = self.pos_tagging(sentence)
            self.pos.append(sent_pos)
            print(self.pos)
            sent_trees = self.build_tree(sent_pos)
            if not sent_trees:
                self.error_message("GrammarError")
                return None
            sent_trees = self.change_tree_labels(sent_trees, sentence)
            self.trees.append(sent_trees)


        print(self.trees)
        for sent in self.trees:
            self.id_syntax_parts(sent)

        for sent in self.parts:
            if not sent:
                self.error_message("VerbError")
                return None

        self.disambiguate_pattern()
        for sent in self.parts:
            if not sent:
                self.error_message("SyntaxError")
                return None
        print(self.parts)

        # self.disambiguate_object()
        return self.parts

    def preparse(self):
        self.text = self.text.lower()
        return self.text

    def tokenize(self):
        nltk.tokenize.punkt.PunktLanguageVars.sent_end_chars = self.sent_separators
        words = []
        sentences = tok.sent_tokenize(self.text)
        for ind, sent in enumerate(sentences):
            sent_words = tok.word_tokenize(sent)
            if sent_words[0].capitalize() not in self.game_actors:
                if ind > 0:
                    sent_ = [words[0][0]]
                else:
                    sent_ = ["I"]
                start_ = 0
            else:
                sent_ = [sent_words[0].capitalize()]
                start_ = 1

            for word in sent_words[start_:]:
                if word not in self.sent_separators and word not in string.punctuation:
                    sent_.append(word)
            words.append(sent_)
        return words

    def pos_tagging(self, sentence):
        pos_tags_and_words = nltk.pos_tag(sentence)
        pos_tags = [x[1] for x in pos_tags_and_words]
        return pos_tags

    def build_tree(self, sent_pos):
        try:
            trees = self.parser.parse(sent_pos)
        except ValueError:
            return None
        Trees = []
        for tree in trees:
            Trees.append(tree)
        if not Trees:
            return None
        return Trees

    def change_tree_labels(self, trees, words):
        new_trees = []
        for tree in trees:
            self.temp_words = [w for w in words]
            # print(trees)
            ntree = self.traverse_in_order(tree)
            new_trees.append(tree)
        return new_trees

    def traverse_in_order(self, tree):
        for index, subtree in enumerate(tree):
            subsub = subtree[0]
            if type(subtree) == tuple:
                if subtree[1] == self.temp_words[0]:
                    self.temp_words.pop(0)
                break
            if type(subsub) == str:
                lbl = subtree.label()
                w = self.temp_words[0]
                self.temp_words.pop(0)
                subtree = (lbl, w)
                tree[index] = subtree
            else:
                self.traverse_in_order(subtree)
        return tree

    def id_syntax_parts(self, trees):
        self.parts.append([])
        for tree in trees:
            d = {"Actor": None, "Verb": None, "Object": None, "Qualifier": None, "Indirect": None}
            for subtree in tree:
                if type(subtree) == tuple:
                    label = subtree[0]
                    sub = subtree[1]
                else:
                    label = subtree.label()
                    sub = subtree
                if label == "C":
                    actor = [vp.leaves() for vp in list(subtree.subtrees())][0][0][1]
                    d["Actor"] = self.game_actors[actor]
                elif label == "V":
                    verb_parts = [x[1] for x in [vp.leaves() for vp in list(subtree.subtrees())][0]]
                    verb = " ".join(verb_parts)
                    for v in self.game_verbs.keys():
                        if verb in self.game_verbs[v].forms:
                            d["Verb"] = self.game_verbs[v]
                            break
                elif label == "O":
                    if sub:
                        obj_parts = [x for x in [vp.leaves() for vp in list(sub.subtrees())][0]]
                    else:
                        obj_parts = None

                    d["Object"] = obj_parts
                elif label == "I":
                    prep = None
                    sub = None
                    for i, t in enumerate(subtree):
                        if i == 0:
                            prep = t[1]
                        else:
                            sub = [x for x in [vp.leaves() for vp in list(t.subtrees())][0]]
                    d["Qualifier"] = prep
                    d["Indirect"] = sub

            if d["Verb"]:
                self.parts[-1].append(d)

    def disambiguate_pattern(self):
        for s_index, sent in enumerate(self.parts):
            for t_index, tree in enumerate(sent):
                pattern = ""
                if tree["Object"]:
                    pattern += "O"
                if tree["Qualifier"]:
                    pattern += "Q"
                if tree["Indirect"]:
                    pattern += "I"
                if pattern not in tree["Verb"].patterns:
                    sent.pop(t_index)
                    self.parts[s_index] = sent

    def disambiguate_object(self):
        for s_index, sent in enumerate(self.parts):
            for t_index, tree in enumerate(sent):
                obj = tree["Object"]
                if obj:
                    pass

    def error_message(self, error_type):
        if error_type == "GrammarError":
            print("I could not understand your command.")
        if error_type == "VerbError":
            print("I could not understand this verb.")
        if error_type == "SyntaxError":
            print("This is the incorrect syntax for this verb.")


if __name__ == "__main__":

    parser = Parser(custom_load("actors.json"), custom_load("verbs.json"))
    while True:
        text = input("> ")
        parser.run_parser(text)
        if text == "quit":
            break
