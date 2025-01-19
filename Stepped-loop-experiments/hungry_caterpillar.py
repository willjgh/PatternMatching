from stepped_mj.node import Sequential, Markov, Limit, Random
from stepped_mj.rule import Rule
from stepped_mj.model import model

# define program
program_hungry_caterpillar = [
    Rule("WWW", "REO"),
    Limit(
        Rule("OWW", "EEO"),
        limit = 4
    ),
    Limit(
        Rule("W", "I"),
        limit = 10
    ),
    Markov(
        Rule("RWI", "EER"),
        Rule("RIW", "EER"),
        #Rule("E**/RBB", "B**/WWR"),
        Rule("RWW/*I*", "EER/*W*"),
        Limit(
            Rule("RWW", "EER"),
            Rule("OEE", "WWO"),
            #Rule("WWWWW/WWWWW/WWWWW", "*****/**I**/*****")
        )
    )
    #Sequential(
    #    Rule("RBB", "WWR"),
    #    Rule("OWW", "BBO")
    #)
]

# define state constructor
def initial_dict_func(grid_height, grid_width):
    return {'W': [(i, j) for i in range(grid_height) for j in range(grid_width)]}

# run model
model(
    program           = program_hungry_caterpillar,
    initial_dict_func = initial_dict_func,
    initial_grid_func = None,
    grid_height       = 15,
    grid_width        = 15,
    window_height     = 500,
    window_width      = 500,
    ticks = 30
)
