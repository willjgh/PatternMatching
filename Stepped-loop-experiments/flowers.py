from stepped_mj.node import Sequential, Markov, Limit, Random
from stepped_mj.rule import Rule
from stepped_mj.model import model

# define program
program_flowers = [
    Limit(Rule("UUUUU/UUUUU/UUUUU/GGGGG/NNNNN", "UUUUU/UUPUU/UUEUU/GGEGG/NNENN")),
    Sequential(
        Rule("UUU/UUU/UPU", "UUU/UPU/UEU"),
        Rule("UUU/UUU/UUU/PUU/**U", "UUU/UPU/UEU/EEU/**U", symmetry="14"),
        Rule("UUUUU/UUUUU/UUUUU/UUPUU/U***U", "UUUUU/UPUPU/UEUEU/UEEEU/U***U"),
        Rule("UUU/UPU/UEU/UEU", "UYU/YEY/UYU/UEU"),
        Rule("UUUUU/UUUUU/UUUUU/GGGGG/NNNNN", "UUUUU/UUPUU/UUEUU/GGEGG/NNENN")
    ),
    Markov(Rule("***/*P*/***", "*Y*/YEY/*Y*"))
]

# define state constructor
def initial_dict_func(grid_height, grid_width):
    initial_dict = {
        'G': [],
        'N': [],
        'U': []
    }
    for i in range(grid_height):
        for j in range(grid_width):
            if i == grid_height - 4:
                # 4th row from bottom green
                initial_dict['G'].append((i, j))
            elif i > grid_height - 4:
                # below 4th row from bottom brown
                initial_dict['N'].append((i, j))
            else:
                # else blue
                initial_dict['U'].append((i, j))
    return initial_dict

# run model
model(
    program           = program_flowers,
    initial_dict_func = initial_dict_func,
    initial_grid_func = None,
    grid_height       = 30,
    grid_width        = 30,
    window_height     = 500,
    window_width      = 500
)
