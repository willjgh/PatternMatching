import numpy as np
from profilehooks import profile

from node import Node
from rule import Rule

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
        self.index_list = [0]

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

        #print(f"Index list: {self.index_list}")
        #print(f"Program: {self.program}")

        # default to no changed indices
        changed_indices = None

        # iterate over index list to identify parent and child / current item
        depth = len(self.index_list)

        parent_item = None
        current_item = self.program[self.index_list[0]]

        for i in range(1, depth):

            parent_item = current_item
            current_item = parent_item[self.index_list[i]]

        # current item Node
        if isinstance(current_item, Node):

            # exhausted Node
            if current_item.flag_exhausted:

                # if parent exists: update flags for changes in current loop / overall
                if parent_item:
                    parent_item.flag_current_loop = current_item.flag_overall_loop
                    parent_item.flag_overall_loop = current_item.flag_overall_loop

                # reset Node flags
                current_item.flag_exhausted = False
                current_item.flag_current_loop = False
                current_item.flag_overall_loop = False

            # non-exhausted Node
            else:
                
                # update index to point to contents
                self.index_list.append(0)

                # Return no changes
                return None, True

        # current item Rule
        else:

            # run Rule
            self.state, changed_indices, flag = current_item.run(self.state)

            # if parent exists: update flags for changes in current loop / overall
            if parent_item:
                if flag: parent_item.flag_current_loop = True
                if flag: parent_item.flag_overall_loop = True

        # for remaining Rule and exhausted Nodes: update index

        # no parent: in program level, increment or terminate
        if not parent_item:

            # get program size
            size = len(self.program)

            # at end: terminate
            if self.index_list[-1] + 1 == size:
                return changed_indices, False
            
            # otherwise: increment
            else:
                self.index_list[-1] += 1

        # sequential Node parent
        elif parent_item.ntype == "Sequential":

            # get contents size
            size = len(parent_item.contents)

            # at end
            if self.index_list[-1] + 1 == size:

                # changes in current loop
                if parent_item.flag_current_loop:

                    # reset index to start
                    self.index_list[-1] = 0

                    # reset loop flag
                    parent_item.flag_current_loop = False

                # no changes in current loop
                else:

                    # point index to parent
                    self.index_list.pop()

                    # exhuast (now pointed to) parent Node
                    parent_item.flag_exhausted = True

            # otherwise: increment
            else:
                self.index_list[-1] += 1

        # markov Node parent
        elif parent_item.ntype == "Markov":
            
            # changes by current item
            if parent_item.flag_current_loop:

                # reset index to start
                self.index_list[-1] = 0

                # reset loop flag
                parent_item.flag_current_loop = False

            # no changes by current item
            else:

                # get contents size
                size = len(parent_item.contents)

                # at end
                if self.index_list[-1] + 1 == size:

                    # point index to parent
                    self.index_list.pop()

                    # exhuast (now pointed to) parent Node
                    parent_item.flag_exhausted = True

                # otherwise: increment
                else:
                    self.index_list[-1] += 1

        elif parent_item.ntype == "Limit":
            pass

        elif parent_item.ntype == "Random":
            pass

        # return changed indices, program status
        return changed_indices, True

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