import nltk
from nltk import tokenize as tok
import string
from errors import *
import json


def remove_duplicates(lst):
    """
    This function removes all duplicate object from a list.
    :param lst: A list.
    :return: The same list, with all its elements appearing just once.
    """
    if len(lst) == 1:
        return lst
    return [i for n, i in enumerate(lst) if i not in lst[:n]]


class PreParser:
    """
        The PreParser class is responsible for identifying the type of the command that is
        provided by the player, and some basic pre-processing before parsing.
    """
    def __init__(self):
        self.text = None
        self.cmd_type = None

    def run_preparser(self, text):
        self.text = text
        self.pre_process()
        self.cmd_type = self.id_command_type()

    def id_command_type(self):
        cmd_type = "Command"
        if self.text in ["quit", "q"]:
            return "Quit"
        if self.text in ["help", "h"]:
            return "Help"
        if self.text in ["undo", "u", "oops"]:
            return "Undo"
        if self.text in ["save", "s"]:
            return "Save"
        return cmd_type

    def pre_process(self):
        """
        This function processes the text before parsing.
        :return:
        """
        self.text = self.text.lower()
        self.text = self.text.strip()


class Parser:
    """
        The Parser class is responsible for analyzing the commands that the player types
        in the game prompt. It then matches the syntactic parts of the sentence, with
        the various Actors, Verbs, and other Entities in the game.
    """
    def __init__(self, game):
        """
        The constructor of the Parser Class.
        :param game: An instance of the Game class.
        """
        # Load custom Context Free Grammar from file and create a ChartParser NLTK object.
        self.parser = nltk.ChartParser(nltk.data.load('file:Grammar/grammar.cfg'))
        self.game = game
        # Symbols/Words that can separate sentences.
        self.sent_separators = ('.', '?', '!', ',', 'then', ';')
        with open("Grammar/qualifiers.json", "r") as file:
            self.qualifier_types = json.load(file)
        # The text given in the prompt by the user.
        self.text = ""
        # A list of the words/tokens in the text
        self.words = []
        # POS tags of the tokens.
        self.pos = []
        # The syntax trees of the sentences in the text.
        self.trees = []
        # The syntactic parts of the sentences in the text.
        self.parts = []

    def run_parser(self, text):
        """
        The function that initiates the text analysis.
        :param text: The text given in the prompt by the user.
        :return: Returns self.parts, which is a list of all sentences in :param text:
                 with each sentence being a dictionary, with keys {"Actor", "Verb", "Object",
                 "Qualifier", "Indirect"} and values being Verb and Entity objects of the game.
        """
        self.text = text
        self.words = self.tokenize()
        self.pos = []
        self.trees = []
        self.parts = []

        # Building the syntactic trees for each sentence.
        for sentence in self.words:
            sent_pos = self.pos_tagging(sentence)
            for actor in self.game.actors.values():
                if actor.reference_noun == sentence[-1]:
                    sent_pos[-1] = "NNP"
            self.pos.append(sent_pos)
            sent_trees = self.build_tree(sent_pos)
            # If the grammar fails to create a tree, there is a GrammarError.
            if not sent_trees:
                raise ParserError("GrammarError")
            trees = []
            tree_count = 0
            for tree in sent_trees:
                trees.append(tree)
                tree_count += 1
            if tree_count == 0:
                raise ParserError("GrammarError")

            # Tree labels are changed from POS Tags to (POS, word) tuples.
            trees = self.change_tree_labels(trees, sentence)
            self.trees.append(trees)

        # Identify the syntactic parts of sentences.
        for sent in self.trees:
            self.id_syntax_parts(sent)

        # Delete all sentences without any valid trees left, delete all duplicates.
        for s_index, sent in enumerate(self.parts):
            sent = [t for t in sent if t]
            if not sent:
                # If a sentence is left without valid trees, raise a Verb Error.
                raise ParserError("VerbError")
            sent = remove_duplicates(sent)
            self.parts[s_index] = sent

        # Check if the sentence structure conforms to the verb syntax patterns.
        self.disambiguate_pattern()

        # Delete all sentences without any valid trees left, delete all duplicates.
        for s_index, sent in enumerate(self.parts):
            sent = [t for t in sent if t]
            if not sent:
                # If a sentence is left without valid trees, raise a Syntax Error.
                raise ParserError("SyntaxError")
            sent = remove_duplicates(sent)
            self.parts[s_index] = sent

        # Identify the game entities in the sentences' object and indirect (object)
        # If there are no valid corresponding entities, delete the tree.
        for s_index, sent in enumerate(self.parts):
            for t_index, tree in enumerate(sent):
                if tree["Object"]:
                    np = self.disambiguate_noun_phrase(tree["Object"])
                    if np:
                        self.parts[s_index][t_index]["Object"] = np
                    else:
                        self.parts[s_index][t_index] = None
                        continue
                if tree["Indirect"]:
                    np = self.disambiguate_noun_phrase(tree["Indirect"])
                    if np:
                        self.parts[s_index][t_index]["Indirect"] = np
                    else:
                        self.parts[s_index][t_index] = None

        # Delete all sentences without any valid trees left, delete all duplicates.
        for s_index, sent in enumerate(self.parts):
            sent = [t for t in sent if t]
            if not sent:
                # If a sentence is left without valid trees, raise an Entity Error
                raise ParserError("EntityError")
            sent = remove_duplicates(sent)
            self.parts[s_index] = sent

        return self.parts

    def tokenize(self):
        """
        This method devides the text into sentences, and each sentence into words.
        :return: list of lists, each list is a sentence, and its elements are the sentence's tokens
        """
        nltk.tokenize.punkt.PunktLanguageVars.sent_end_chars = self.sent_separators
        words = []
        sentences = tok.sent_tokenize(self.text)
        for ind, sent in enumerate(sentences):
            sent_words = tok.word_tokenize(sent)
            # If the first word of the sentence is not a game actor, the parser supposes it it "I"
            if sent_words[0].capitalize() not in self.game.actors:
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
        """
        This method returns the Part-Of-Speech tags of a sentence.
        :param sentence: list of tokens
        :return: a list of the sentence's POS tags
        """
        pos_tags_and_words = nltk.pos_tag(sentence)
        pos_tags = [x[1] for x in pos_tags_and_words]
        return pos_tags

    def build_tree(self, sent_pos):
        """
        This function parses through the sentences, using the custom grammar and the NLTK parser.
        :param sent_pos: A list of a sentences POS tags.
        :return: A list containing all the NLTK trees of the sentence.
        """
        try:
            trees = self.parser.parse(sent_pos)
        except ValueError:
            return None
        if not trees:
            return None
        return trees

    def change_tree_labels(self, trees, words):
        """
        This function replaces all the POS tags in the trees with (POS, word) tuples.
        :param trees: The syntax trees of a sentence.
        :param words: The words of a sentence.
        :return: The syntax trees with their leaf nodes replaced.
        """
        new_trees = []
        for tree in trees:
            self.temp_words = [w for w in words]
            self.traverse_in_order(tree)
            new_trees.append(tree)
        return new_trees

    def traverse_in_order(self, tree):
        """
        In order traversal of the tree nodes and replacement with the corresponding POS, word tuple.
        :param tree: A syntax tree.
        """
        for index, subtree in enumerate(tree):
            subsub = subtree[0]
            if type(subtree) == tuple:
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

    def id_syntax_parts(self, trees):
        """
        This method identifies the parts of each syntax tree and matches the Subject and the Verb of the sentence
        with their corresponding Actor and Verb object.
        :param trees:
        :return:
        """
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
                    d["Actor"] = self.game.actors[actor]
                elif label == "V":
                    verb_parts = [x[1] for x in [vp.leaves() for vp in list(subtree.subtrees())][0]]
                    verb = " ".join(verb_parts)
                    for v in self.game.verbs.keys():
                        if verb in self.game.verbs[v].forms:
                            d["Verb"] = self.game.verbs[v]
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
                    d["Qualifier"] = self.disambiguate_qualifier(prep)
                    d["Indirect"] = sub

                elif label == "J" or label == "B":
                    prep = subtree[1]
                    d["Qualifier"] = self.disambiguate_qualifier(prep)

            # Only the trees with a valid Verb object are added back to the list.
            if d["Verb"]:
                self.parts[-1].append(d)

    def disambiguate_pattern(self):
        """
        This method identifies the syntax pattern of the sentence and matches it against the syntax
        patterns that the Verb object can appear in.
        :return: None.
        """
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
                    sent[t_index] = None
                    self.parts[s_index] = sent

    def disambiguate_qualifier(self, qualifier):
        if not qualifier:
            return None
        q_dict = self.qualifier_types
        for category in q_dict.keys():
            if qualifier in q_dict[category]:
                return category
        return qualifier.capitalize()

    def disambiguate_noun_phrase(self, noun_phrase):
        """
        This function identifies the game Entity objects in a noun phrase.
        :param noun_phrase: NLTK tree of a noun phrase.
        :return: A list of all Entity objects in the noun phrase.
        """
        things = [{"Noun": None, "Adjectives": []}]
        for word in reversed(noun_phrase):
            if word[0] == 'A':
                continue
            elif word[0] == 'L':
                things.append({"Noun": None, "Adjectives": []})
            else:
                if not things[-1]["Noun"]:
                    things[-1]["Noun"] = word[1]
                else:
                    things[-1]["Adjectives"].append(word[1])

        entity_list = []
        for thing in things:
            entity = None
            for g_thing in self.game.things.keys():
                if self.game.things[g_thing].reference_noun == thing["Noun"]:
                    match = True
                    if self.game.things[g_thing].__class__.__name__ == "Actor":
                        entity = self.game.things[g_thing]
                    else:
                        for adj in thing["Adjectives"]:
                            if adj not in self.game.things[g_thing].reference_adjectives:
                                match = False
                                break
                        if not match:
                            continue
                        else:
                            entity = self.game.things[g_thing]
                else:
                    continue
            if not entity:
                return None
            else:
                entity_list.append(entity)
        entity_list.reverse()
        return entity_list


