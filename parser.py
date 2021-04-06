import nltk
from nltk import tokenize as tok
import string
import os

import things
import verbs
import actors
import game

Grammar = nltk.data.load('file:grammar.cfg')


class Parser:

    def __init__(self, text):
        self.text = text
        self.sent_separators = ('.', '?', '!', ',', 'then', ';')
        self.text = self.preparse()
        self.words = self.tokenize()
        self.parser = nltk.ChartParser(Grammar)
        self.pos = []
        self.trees = []
        self.parts = []
        for sentence in self.words:
            sent_pos = self.pos_tagging(sentence)
            self.pos.append(sent_pos)
            sent_trees = self.build_tree(sent_pos)
            if not sent_trees:
                self.error_message("GrammarError")
                return
            sent_trees = self.change_tree_labels(sent_trees, sentence)
            self.trees.append(sent_trees)

        for sent in self.trees:
            self.id_syntax_parts(sent)

    def preparse(self):
        self.text = self.text.lower()
        return self.text

    def tokenize(self):
        nltk.tokenize.punkt.PunktLanguageVars.sent_end_chars = self.sent_separators
        words = []
        sentences = tok.sent_tokenize(self.text)
        for ind, sent in enumerate(sentences):
            sent_words = tok.word_tokenize(sent)
            # CHANGE THIS CURRENT_GAME THING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if sent_words[0].capitalize() not in game.CURRENT_GAME.actors:
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
        Trees = []
        for tree in trees:
            self.temp_words = [w for w in words]
            self.traverse_in_order(tree)
            Trees.append(tree)
        return Trees

    def traverse_in_order(self, tree):
        for index, subtree in enumerate(tree):
            subsub = subtree[0]
            if type(subtree) == tuple:
                break
            if type(subsub) == str:
                lbl = subtree.label()
                w = self.temp_words[0]
                self.temp_words.pop(0)
                subtree = (lbl, w)
                tree[index] = subtree
            else:
                self.traverse_in_order(subtree)

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
                    d["Actor"] = [vp.leaves() for vp in list(subtree.subtrees())][0][0][1]
                elif label == "V":
                    verb_parts = [x[1] for x in [vp.leaves() for vp in list(subtree.subtrees())][0]]
                    d["Verb"] = " ".join(verb_parts)
                elif label == "O":
                    d["Object"] = sub
                elif label == "I":
                    prep = None
                    sub = None
                    for i, t in enumerate(subtree):
                        if i == 0:
                            prep = t[1]
                        else:
                            sub = t
                    d["Qualifier"] = prep
                    d["Indirect"] = sub

            self.parts[-1].append(d)

    def error_message(self, error_type):

        if error_type == "GrammarError":
            print("I could not understand your command.")


class Interpreter:
    def __init__(self, sent_components):
        self.components = sent_components
        self.actor_cand = self.components["Actor"]
        self.verb_cand = self.components["Verb"]
        self.object_cand = self.components["Object"]
        self.qualifier_cand = self.components["Qualifier"]
        self.indirect_cand = self.components["Indirect"]

    def disambiguate_actor(self):
        pass

    def disambiguate_verb(self):
        pass

    def disambiguate_object(self):
        pass

    def disambiguate_qualifier(self):
        pass

    def disambiguate_ind_object(self):
        pass

    def error_message(self, error_type):
        if error_type == "ActorNotKnownError":
            print("There is no character named %s." % self.actor_cand)
        if error_type == "ActorMissingError":
            print("%s is not in the room" % self.actor_cand.capitalize())
        if error_type == "ActorNotCommandable":
            print("%s refuses to do what you're asking of them." % self.actor_cand.capitalize())


if __name__ == "__main__":
    while True:
        text = input("> ")
        parser = Parser(text)
        print(parser.parts)

        if text == "quit":
            break

    os.system("pause")

