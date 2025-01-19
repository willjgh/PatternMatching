from stepped_mj.node import Sequential, Markov, Limit, Random
from stepped_mj.rule import Rule
from stepped_mj.model import model

# define program
program_paths = [
    Limit(
        Limit(
            Rule("B", "W"),
            Rule("B", "R"),
            limit=2
        ),
        Sequential(
            Rule("WB", "WW"),
            Rule("RB", "RR")
        ),
        Markov(
            Rule("WR", "AB", rtype="prl"),
            Rule("W", "B", rtype="prl"),
            Rule("R", "B", rtype="prl")
        ),
        limit = 3
    ),
    Rule("B", "F", rtype="prl")
]

# define state constructor
def initial_dict_func(grid_height, grid_width):
    return {'B': [(i, j) for i in range(grid_height) for j in range(grid_width)]}

# run model
model(
    program           = program_paths,
    initial_dict_func = initial_dict_func,
    initial_grid_func = None,
    grid_height       = 30,
    grid_width        = 30,
    window_height     = 500,
    window_width      = 500,
    ticks             = 60
)