from stepped_mj.node import Sequential, Markov, Limit, Random
from stepped_mj.rule import Rule
from stepped_mj.model import model

# define program
program_river = [
    Limit(
        Rule("B", "W"),
        Rule("B", "R"),
        limit = 3
    ),
    Sequential(
        Rule("WB", "WW"),
        Rule("RB", "RR")
    ),
    Markov(Rule("WR", "UU", rtype="prl")),
    Sequential(
        Rule("W", "B", rtype="prl"),
        Rule("R", "B", rtype="prl")
    ),
    Markov(Rule("UB", "UY")),
    Markov(Rule("Y", "U")),
    Markov(Rule("UB", "UG")),
    Limit(
        Rule("B", "E"),
        limit = 13
    ),
    Sequential(
        Rule("GB", "GG"),
        Rule("EB", "EE")
    )
]

# define state constructor
def initial_dict_func(grid_height, grid_width):
    return {'B': [(i, j) for i in range(grid_height) for j in range(grid_width)]}

# run model
model(
    program           = program_river,
    initial_dict_func = initial_dict_func,
    initial_grid_func = None,
    grid_height       = 30,
    grid_width        = 30,
    window_height     = 500,
    window_width      = 500
)
