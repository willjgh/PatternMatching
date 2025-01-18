from stepped_mj.node import Sequential, Markov, Limit, Random
from stepped_mj.rule import Rule
from stepped_mj.model import model

# define program
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

# define state constructor
def initial_dict_func(grid_height, grid_width):
    return {'B': [(i, j) for i in range(grid_height) for j in range(grid_width)]}

# run model
model(
    program           = program_competition,
    initial_dict_func = initial_dict_func,
    initial_grid_func = None,
    grid_height       = 30,
    grid_width        = 30,
    window_height     = 500,
    window_width      = 500
)
