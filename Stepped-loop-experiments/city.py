from stepped_mj.node import Sequential, Markov, Limit, Random
from stepped_mj.rule import Rule
from stepped_mj.model import model

# program settings
towers = 50
width = 15

# define program
program_city = [
    Limit(
        Rule("B", "R"),
        Limit(
            Rule("RB", "RR", symmetry="14"),
            limit = width
        ),
        Markov(Rule("R", "D")),
        limit = towers
    ),
    Markov(
        Rule("DB/BB", "DB/DB", symmetry="14", rtype="prl"),
        Rule("DD/DB", "DD/DA", symmetry="14", rtype="prl"),
        Rule("AB", "AA", symmetry="1347", rtype="prl"),
        Rule("B", "U", rtype="prl")
    )
]

# define state constructor
def initial_dict_func(grid_height, grid_width):
    return {'B': [(i, j) for i in range(grid_height) for j in range(grid_width)]}

# run model
model(
    program           = program_city,
    initial_dict_func = initial_dict_func,
    initial_grid_func = None,
    grid_height       = 200,
    grid_width        = 100,
    window_height     = 1000,
    window_width      = 500
)
