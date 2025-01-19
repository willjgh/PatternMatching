from stepped_mj.node import Sequential, Markov, Limit, Random
from stepped_mj.rule import Rule
from stepped_mj.model import model

# define program

# construct cellular automata rules from binary code
bin_code = "00010110"

# rules
cellular_rules = []

# input patterns
cellular_inputs = [
    "PPP/",
    "PPK/",
    "PKP/",
    "PKK/",
    "KPP/", 
    "KPK/",
    "KKP/",
    "KKK/"
]

for i in range(8):

    # binary code letter i
    cout = ["Y", "O"][int(bin_code[i])]

    # cellular input
    cinp = cellular_inputs[i] 

    # complete rule
    cellular_rules.append([cinp + "*U*", cinp  + "*" + cout + "*"])

# program
program_ca = [
    # repeat for each row
    Sequential(
        # apply cellular rules to pink and purple to produce yellow and orange
        Sequential(
            *[Rule(cellular_rule[0], cellular_rule[1], symmetry="1", rtype="prl") for cellular_rule in cellular_rules]
        ),
        # fill below ends with same colour as above
        Rule("K/U", "K/Y", symmetry="1", rtype="prl"),
        Rule("P/U", "P/O", symmetry="1", rtype="prl"),
        # turn pink and purple to white and black
        Rule("K", "W", rtype="prl"),
        Rule("P", "B", rtype="prl"),
        # turn yellow and orange to pink and purple
        Rule("Y", "K", rtype="prl"),
        Rule("O", "P", rtype="prl")
    )
]

# define state constructor
def initial_dict_func(grid_height, grid_width):
    initial_dict = {
        'P': [],
        'K': [],
        'U': []
    }
    for i in range(grid_height):
        for j in range(grid_width):
            # 1st row: pink with purple centre
            if i == 0:
                if j == grid_width // 2:
                    col = "P"
                else:
                    col = "K"
                # col = np.random.choice(["K", "P"])
                initial_dict[col].append((i, j))
            else:
                # rest blue
                initial_dict['U'].append((i, j))
    return initial_dict

# run model
model(
    program           = program_ca,
    initial_dict_func = initial_dict_func,
    initial_grid_func = None,
    grid_height       = 100,
    grid_width        = 100,
    window_height     = 500,
    window_width      = 500,
    ticks             = 0
)