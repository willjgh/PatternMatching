from stepped_mj.node import Sequential, Markov, Limit, Random
from stepped_mj.rule import Rule
from stepped_mj.model import model

# define program
program_fill = [
    Sequential(Rule("B", "W"))
]
# define state constructor
def initial_dict_func(grid_height, grid_width):
    return {'B': [(i, j) for i in range(grid_height) for j in range(grid_width)]}

# run model
model(
    program           = program_fill,
    initial_dict_func = initial_dict_func,
    initial_grid_func = None,
    grid_height       = 10,
    grid_width        = 10,
    window_height     = 500,
    window_width      = 500,
    ticks             = 60
)
