import numpy as np

class Sequential(Node):
    def __init__(self, *args):

        # contents: collection of rules or other nodes
        self.contents = list(args)

class Markov(Node):
    def __init__(self, *args):

        # contents: collection of rules or other nodes
        self.contents = list(args)

class Limit(Node):
    def __init__(self, *args, limit=1):
        
        # contents: collection of rules or other nodes
        self.contents = list(args)

        # limit: limit on loops over contents
        self.limit = limit

class Random(Node):
    def __init__(self, *args):

        # contents: collection of rules or other nodes
        self.contents = list(args)


class Node():
    def __init__(self, ntype, contents, limit=None):

        # define node type: Markov, Sequential, Limit
        self.ntype = ntype

        # define contents: list of rules or other nodes (allows nesting)
        self.contents = contents

        # for limit nodes: limit on the number of times contents are called 
        self.limit = limit

        # flag for changes in the current loop over contents
        self.flag_current_loop = False

        # flag for changes overall
        self.flag_overall_loop = False

        # flag for exhaustion
        self.flag_exhausted = False

    def run(self, state):
        '''Loop over contents according to type and call them on grid'''

        # random generator
        rng = np.random.default_rng()

        # overall flag for any item's execution
        overall_flag = False

        # Markov node: loop over contents and run until one executes, then repeat from beginning
        if self.ntype == "Markov":

            # loop while at least one content executed (end node call otherwise)
            exec_flag = True
            while exec_flag:

                # reset flag
                exec_flag = False

                # loop over contents
                for item in self.contents:

                    # run item: recieve updated state and flag for execution
                    state, flag = item.run(state)

                    # if item executed: toggle flags, reset loop over node content
                    if flag:
                        overall_flag = True
                        exec_flag = True
                        break

        # Sequential node: loop over contents regardless of execution
        elif self.ntype == "Sequential":

            # loop while at least one content executed (end node call otherwise)
            exec_flag = True
            while exec_flag:

                # reset flag
                exec_flag = False

                # loop over contents
                for item in self.contents:

                    # run item: recieve updated state and flag for execution
                    state, flag = item.run(state)

                    # if item executed: toggle flags
                    if flag:
                        overall_flag = True
                        exec_flag = True

        # Limit node: run each item in contents a limited number of times
        elif self.ntype == "Limit":

            # tuple given as limit: sample from uniform distribution
            if isinstance(self.limit, tuple):

                limit = rng.integers(*self.limit)

            # integer given: proceed as usual
            else:

                limit = self.limit

            # limited number of runs
            for i in range(limit):

                # loop over contents
                for item in self.contents:

                    # run item: recieve updated state and flag for executioon
                    state, flag = item.run(state)

                    # if item executed: toggle flag
                    if flag:
                        overall_flag = True

        # Random node: execute items at random
        elif self.ntype == "Random":

            # loop while at least one content executed
            exec_flag = True
            while exec_flag:

                # reset flag
                exec_flag = False

                # shuffle contents
                rng.shuffle(self.contents)

                # loop over shuffled contents until one executes
                for item in self.contents:

                    # run item: recieve updated state and flag for execution
                    state, flag = item.run(state)

                    # if item executed: toggle flag, reset loop over node contents
                    if flag:
                        overall_flag = True
                        exec_flag = True
                        break

        # return updated state and flag for execution (of any item)
        return state, overall_flag