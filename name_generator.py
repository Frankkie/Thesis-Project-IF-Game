import os
import numpy as np

import nltk
from nltk.parse import ChartParser


class NameGenerator:
    """

    """
    def __init__(self, seed, grammar, prefix=''):
        path = os.path.join('Grammar', grammar)
        path = 'file:' + path
        self.seed = seed

        grammar = nltk.data.load(path)
        chart_parser = ChartParser(grammar)
        self.grammar = chart_parser.grammar()
        self.prefix = prefix
        self.generated = set()

    def generate_name(self, seed):
        name = self.generate_sample(seed)
        name[0] = name[0].capitalize()
        name = ''.join(name)
        name = self.prefix + name
        if name in self.generated:
            return self.generate_name(seed+1)
        return name

    def rewrite_at(self, index, replacements, the_list):
        del the_list[index]
        the_list[index:index] = replacements

    def generate_sample(self, seed):
        np.random.seed(seed + self.seed)
        sentence_list = [self.grammar.start()]
        all_terminals = False
        while not all_terminals:
            all_terminals = True
            for position, symbol in enumerate(sentence_list):
                if symbol in self.grammar._lhs_index:
                    all_terminals = False
                    derivations = self.grammar._lhs_index[symbol]
                    derivation = np.random.choice(derivations)
                    self.rewrite_at(position, derivation.rhs(), sentence_list)
        return sentence_list


if __name__ == "__main__":
    star_name_gen = NameGenerator(0, 'star_name_grammar.cfg', prefix='Andromeda')

    for i in range(100):
        print(star_name_gen.generate_name(i))

