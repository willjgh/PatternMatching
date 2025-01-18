import numpy as np

# create generator
rng = np.random.default_rng()


class Node():
    def __init__(self, ntype, contents):

        # define node type: Markov, Sequential, Limit
        self.ntype = ntype

        # define contents: list of rules or other nodes (allows nesting)
        self.contents = contents

        # flag for changes in the current loop over contents
        self.flag_current_loop = False

        # flag for changes overall
        self.flag_overall_loop = False

        # flag for exhaustion
        self.flag_exhausted = False

    def reset(self):
        '''Reset Node flags and settings.'''
        self.flag_current_loop = False
        self.flag_overall_loop = False
        self.flag_exhausted = False

    def __getitem__(self, key):
        '''Allow indexing of contents.'''
        return self.contents[key]
    
    def __setitem__(self, key, val):
        '''Allow setting contents via indexing.'''
        self.contents[key] = val


class Sequential(Node):
    def __init__(self, *args):
        super().__init__("Sequential", list(args))


class Markov(Node):
    def __init__(self, *args):
        super().__init__("Markov", list(args))


class Limit(Node):
    def __init__(self, *args, limit=1):
        super().__init__("Limit", list(args))

        # limit
        self.limit = limit

        # current count
        self.current_count = 0

    def reset(self):
        super().reset()

        # reset current count
        self.current_count = 0


class Random(Node):
    def __init__(self, *args):

        # initial shuffle of contents
        rng.shuffle(list(args))

        # constuct Node
        super().__init__("Random", list(args))