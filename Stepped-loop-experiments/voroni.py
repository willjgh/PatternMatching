from stepped_mj.node import Sequential, Markov, Limit, Random
from stepped_mj.rule import Rule
from stepped_mj.model import model

# define program
program_voroni = [
    Rule("B", "W"),
    Rule("B", "R"),
    Sequential(
        Rule("WB", "WW"),
        Rule("RB", "RR")
    )
]
# define state constructor
def initial_dict_func(grid_height, grid_width):
    return {'B': [(i, j) for i in range(grid_height) for j in range(grid_width)]}

# run model
model(
    program           = program_voroni,
    initial_dict_func = initial_dict_func,
    initial_grid_func = None,
    grid_height       = 20,
    grid_width        = 20,
    window_height     = 500,
    window_width      = 500,
    ticks             = 60
)
