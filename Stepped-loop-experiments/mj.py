import numpy as np
from node import Node

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

# create generator
rng = np.random.default_rng()


class MarkovJunior:

    def __init__(self, grid_height, grid_width, program, initial_grid=None, initial_dict=None):

        # grid size
        self.i = grid_height
        self.j = grid_width

        # program list
        self.program = program

        # index list
        self.index_list = [0]

        # define state: set with initial grid and dict
        self.setup(initial_grid, initial_dict)

        # running status
        self.running = True

    def setup(self, initial_grid, initial_dict):
        '''
        Setup initial state from input grid and/or dict
        '''

        # state
        self.state = {
            'grid': np.empty((self.i, self.j), dtype=str),
            'dict': {colour: [] for colour in colours.keys()}
        }

        # both provided: set
        if initial_grid and initial_dict:
            self.state['grid'] = initial_grid
            for colour, index_list in initial_dict.items():
                self.state['dict'][colour] = index_list

        # only grid provided: populate dict
        elif initial_grid:
            self.state['grid'] = initial_grid
            for i in range(self.i):
                for j in range(self.j):
                    self.state['dict'][initial_grid[i, j]].append((i, j))

        # only dict provided: populate grid, and fill dict
        elif initial_dict:
            for colour, index_list in initial_dict.items():
                self.state['dict'][colour] = index_list
                for index in index_list:
                    self.state['grid'][index[0], index[1]] = colour

        # none provided
        else:
            raise NotImplementedError

    def next(self):
        '''Step iteration of program.'''

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

                # reset Node
                current_item.reset()

            # non-exhausted Node
            else:
                
                # update index to point to contents
                self.index_list.append(0)

                # Return no changes
                return None

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

                # set status
                self.running = False

                # return changes
                return changed_indices
            
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
            
            # get contents size
            size = len(parent_item.contents)

            # at end
            if self.index_list[-1] + 1 == size:

                # no changes in current loop OR reach limit
                if (not parent_item.flag_current_loop) or (parent_item.current_count + 1 == parent_item.limit):

                    # point index to parent
                    self.index_list.pop()

                    # exhaust (now pointed to) parent Node
                    parent_item.flag_exhausted = True

                # below limit
                else:

                    # increment count
                    parent_item.current_count += 1

                    # reset index to start
                    self.index_list[-1] = 0

                    # reset loop flag
                    parent_item.flag_current_loop = False

            # otherwise: increment
            else:
                self.index_list[-1] += 1

        elif parent_item.ntype == "Random":
            
            # changes by current item
            if parent_item.flag_current_loop:

                # shuffle parent contents
                rng.shuffle(parent_item.contents)

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

        # return changed indices
        return changed_indices