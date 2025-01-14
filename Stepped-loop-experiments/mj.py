import numpy as np
from profilehooks import profile

from node import Node
from rule import Rule
from display import Display

# dictionary for translating colour alphabet to RGB
colours = {
    "B": (0  , 0  , 0  ),
    "I": (0  , 76 , 153),
    "P": (127, 0  , 255),
    "E": (0  , 153, 76 ),
    "N": (153, 76 , 0  ),
    "D": (96 , 96 , 96 ),
    "A": (192, 192, 192),
    "W": (255, 255, 255),
    "R": (255, 0  , 0  ),
    "O": (255, 165, 0  ),
    "Y": (255, 255, 0  ),
    "G": (0  , 255, 0  ),
    "U": (0  , 255, 255),
    "S": (153, 153, 255),
    "K": (255, 51 , 255),
    "F": (255, 204, 153)
}

class MarkovJunior:

    def __init__(self, i, j, window_width=700, window_height=700, ticks=0):

        # grid size
        self.i = i
        self.j = j

        # define state: grid, dict, game
        self.state = {
            'grid': np.empty((self.i, self.j), dtype=str),
            'dict': {colour: [] for colour in colours.keys()}
        }

        # program list
        self.program = []

        # index list
        self.index_list = []

    def program_setup(self):
        '''
        Define program: nodes and rules, and setup grid

        MarkovJunior class provides an example of a program setup (below)
        '''

        # define state
        for i in range(self.i):
            for j in range(self.j):
                self.state['grid'][i, j] = 'B'
                self.state['dict']['B'].append((i, j))

        # define densities
        #def density_upper_left(state):
        #    return np.array([[-np.log(i * j + 1) for j in range(self.j)] for i in range(self.i)])

        # define program: nodes and their rules
        self.program = [
            Node(
                "Markov", [
                    Node(
                        "Sequential", [
                            Node(
                                "Limit", [
                                    Rule("B", "W", self.state)
                                ],
                                limit = 1
                            ),
                            Node(
                                "Limit", [
                                    Rule("B", "R", self.state)
                                ],
                                limit = 1
                            ),
                            Node(
                                "Sequential", [
                                    Rule("WB", "WW", self.state, rtype="one"),
                                    Rule("RB", "RR", self.state, rtype="one")
                                ]
                            )
                        ]
                    ),
                    Node(
                        "Sequential", [
                            Rule("W", "B", self.state, rtype="one"),
                            Rule("R", "B", self.state, rtype="one")
                        ]
                    )
                ]
            )
        ]

    def next(self):
        '''Step iteration of program.'''

        # move through index list to identify parent item and current item
        depth = len(self.index_list)

        parent_item = None
        current_item = self.program[self.index_list[0]]

        for i in range(1, depth):

            parent_item = current_item
            current_item = parent_item[self.index_list[i]]

        # if current item is a Rule
        if type(current_item) == Rule:

            # run current item (Rule): return updated state and execution flag
            self.state, flag = current_item.run(self.state)

            # update flags of parent item (Node): at least one change in current loop over contents, and overall
            if flag: parent_item.flag_current_loop = True
            if flag: parent_item.flag_overall_loop = True

        # if current item is an exhausted Node
        elif type(current_item) == Node and current_item.flag_exhausted == True:

            # reset exhaustion
            current_item.flag_exhausted = False

            # set flags of parent using current flags
            parent_item.flag_current_loop = self.flag_overall_loop
            parent_item.flag_overall_loop = self.flag_overall_loop

        # if current item is a non-exhausted Node
        elif type(current_item) == Node and current_item.flag_exhausted == False:

            # update index to level of node contents (deeper level)
            self.index_list.append(0)

            # exit
            return None
        
        # for executed rules / exhausted nodes update index according to parent node type

        # size of parent contents
        size = len(parent_item.contents)

        # current index (deepest level)
        idx = self.index_list[-1]

        # update index
        if parent_item.ntype == 'Sequential':

            # at end of parent contents
            if idx + 1 == size:

                # if at least one change made in current loop
                if parent_item.flag_current_loop:

                    # update index to start of parent contents
                    self.index_list[-1] = 0

                # no changes made in current loop
                else:

                    # update index to higher level
                    self.index_list.pop()

            # otherwise: move to next parent content
            else:
                self.index_list[-1] += 1

        # return indices of changes
        return None
                

        



    def program_loop(self):
        '''Run the program'''

        # setup program
        self.program_setup()

        # draw initial grid
        self.state['game'].draw_setup(self.state)

        # iterate through program
        for node in self.program:

            # run node
            self.state, flag = node.run(self.state)

        # program has finished: wait for quit call
        while self.state['game'].running:

            self.state['game'].event_handler()