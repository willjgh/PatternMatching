from mj import MarkovJunior
from node import Node, Sequential, Markov, Limit, Random
from rule import Rule
from multi_display import MultiDisplay
import numpy as np

def main():

    # define multi grid size, canvas / grid size, window size
    multi_height, multi_width = 10, 10
    grid_height, grid_width = 40, 40
    window_height, window_width = 1000, 1000

    # define program list
    program_list = [[None for j in range(multi_width)] for i in range(multi_height)]

    # define index change list
    changed_indices_list = [[None for j in range(multi_width)] for i in range(multi_height)]

    # fill
    for i in range(multi_height):
        for j in range(multi_width):

            # define initial state
            initial_dict = {
                'B': [(i, j) for i in range(grid_height) for j in range(grid_width)]
            }

            program_loop_erased = [
                Rule("B", "R"),
                Sequential(
                    Markov(Rule("RBB", "WWR")),
                    Rule("RBW", "RBO"),
                    Markov(Rule("RWW", "BBR")),
                    Rule("RWO", "BBR")
                )
            ]

            # initialize program
            program_list[i][j] = MarkovJunior(
                                    grid_height,
                                    grid_width,
                                    program_loop_erased,
                                    None,
                                    initial_dict
                                )


    # initialize multi display
    multi_display = MultiDisplay(
        window_height,
        window_width,
        grid_height,
        grid_width,
        multi_height,
        multi_width,
        ticks=0
    )

    # draw intial state
    multi_display.draw_setup(program_list)

    # loop
    while multi_display.running:

        # handle events
        multi_display.event_handler()

        for i in range(multi_height):
            for j in range(multi_width):
        
                # step
                changed_indices = program_list[i][j].next()

                # store changes
                changed_indices_list[i][j] = changed_indices

        # draw changes
        multi_display.draw(program_list, changed_indices_list)

if __name__ == "__main__":
    main()