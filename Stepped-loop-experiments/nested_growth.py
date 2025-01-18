from stepped_mj.node import Sequential, Markov, Limit, Random
from stepped_mj.rule import Rule
from stepped_mj.model import model

# helper function
def star(a, b):
    #return f"*{a}{a}{a}*/{a}{a}{a}{a}{a}/{a}{a}{b}{a}{a}/{a}{a}{a}{a}{a}/*{a}{a}{a}*"
    return f"{a}{a}{a}{a}{a}/{a}{a}{a}{a}{a}/{a}{a}{b}{a}{a}/{a}{a}{a}{a}{a}/{a}{a}{a}{a}{a}"


# define program
program_nested_growth = [
    Sequential(
        Rule("WB", "WW", rtype="all"),
        Rule("AW", "AA", rtype="all"),
        Rule("DA", "DD", rtype="all"),
        Rule("WD", "WW", rtype="all"),
        Rule(star("W","W"), star("W","A"), rtype="all"),
        Rule(star("A","A"), star("A","D"), rtype="all"),
        Rule(star("D","D"), star("D","W"), rtype="all")
    )
]  

# define state constructor
def initial_dict_func(grid_height, grid_width):
    initial_dict = {
        'B': [],
        'W': []
    }
    for i in range(grid_height):
        for j in range(grid_width):
            if i == grid_height // 2 and j == grid_width // 2:
                # middle white
                initial_dict['W'].append((i, j))
            else:
                # else black
                initial_dict['B'].append((i, j))
    return initial_dict

# run model
model(
    program           = program_nested_growth,
    initial_dict_func = initial_dict_func,
    initial_grid_func = None,
    grid_height       = 50,
    grid_width        = 50,
    window_height     = 500,
    window_width      = 500
)
