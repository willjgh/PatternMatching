from stepped_mj.mj import MarkovJunior
from stepped_mj.node import Node, Sequential, Markov, Limit, Random
from stepped_mj.rule import Rule
from stepped_mj.display import Display
import numpy as np

program_competition = [
    Limit(
        Rule("B", "R"),
        Rule("B", "Y"),
        Rule("B", "U"),
        Rule("B", "G"),
        Rule("B", "O")
    ),
    Sequential(
        Rule("RB", "RR"),
        Rule("YB", "YY"),
        Rule("UB", "UU"),
        Rule("GB", "GG"),
        Rule("OB", "OO")
    ),
    Sequential(
        Rule("RY", "RR"),
        Rule("YU", "YY"),
        Rule("UG", "UU"),
        Rule("GO", "GG"),
        Rule("OR", "OO")
    )
]

def main():

    # define a program
    program = program_competition

    # define grid size and window size
    grid_height, grid_width = 50, 50
    window_height, window_width = 500, 500

    # define initial state
    initial_dict = {'B': [(i, j) for i in range(grid_height) for j in range(grid_width)]}

    # initialize mj
    mj = MarkovJunior(
        grid_height,
        grid_width,
        program,
        None,
        initial_dict
    )

    # initialize display
    display = Display(
        window_height,
        window_width,
        grid_height,
        grid_width
    )

    # draw intial state
    display.draw_setup(mj.state)

    # manual start
    display.automatic = False

    # running info
    changed_indices = []

    # loop
    while display.running:

        # handle events
        display.event_handler()

        # only step if program still running
        if mj.running:

            # automatic
            if display.automatic:

                # step
                changed_indices = mj.next()
            
            # manual
            else:

                # check action
                if display.action:
                
                    # step
                    changed_indices = mj.next()

                    # reset action
                    display.action = False

            # draw changes
            if changed_indices:

                display.draw(mj.state, changed_indices)

if __name__ == "__main__":
    main()