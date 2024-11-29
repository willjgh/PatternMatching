from mj import *

class CellularAutomata(MarkovJunior):

    def __init__(self, i, j, window_width=700, window_height=700, ticks=0):
        super().__init__(i, j, window_width=window_width, window_height=window_height, ticks=ticks) 

    def program_setup(self):

        # initial state
        for i in range(self.i):
            for j in range(self.j):

                # 1st row: random pink or purple
                if i == 0:
                    if j == self.j // 2:
                        col = "P"
                    else:
                        col = "K"
                    # col = np.random.choice(["K", "P"])
                    self.state['grid'][i, j] = col
                    self.state['dict'][col].append((i, j))
                else:
                    # rest white
                    self.state['grid'][i, j] = 'U'
                    self.state['dict']['U'].append((i, j))

        # densities

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
        self.program = [
            # repeat for each row
            Node("Sequential", [
                # apply cellular rules to pink and purple to produce yellow and orange
                Node("Sequential", [
                    Rule(cellular_rule[0], cellular_rule[1], self.state, symmetry="1", rtype="prl") for cellular_rule in cellular_rules
                ]),
                # fill below ends with same colour as above
                Rule("K/U", "K/Y", self.state, symmetry="1", rtype="prl"),
                Rule("P/U", "P/O", self.state, symmetry="1", rtype="prl"),
                # turn pink and purple to white and black
                Rule("K", "W", self.state, rtype="prl"),
                Rule("P", "B", self.state, rtype="prl"),
                # turn yellow and orange to pink and purple
                Rule("Y", "K", self.state, rtype="prl"),
                Rule("O", "P", self.state, rtype="prl")
            ])
        ]

@profile
def main():
    cellulautomata = CellularAutomata(200, 200, window_width=700, window_height=700)
    cellulautomata.program_loop()

if __name__ == "__main__":
    main()