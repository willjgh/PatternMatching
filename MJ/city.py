from mj import *

class City(MarkovJunior):

    def __init__(self, i, j):
        super().__init__(i, j)

    def program_setup(self):

        # initial state
        for i in range(self.i):
            for j in range(self.j):
                self.state['grid'][i, j] = 'B'
                self.state['dict']['B'].append((i, j))

        # densities

        # settings
        towers = 5
        width_range = (10, 20)

        # program
        self.program = [
            # for each tower
            Node("Limit", [
                # spawn red seed
                Rule("B", "R", self.state),
                # expand sideways by sampled width
                Node("Limit", [
                    Rule("RB", "RR", self.state, symmetry="14")
                ], limit=width_range),
                # turn completed roof white
                Node("Markov", [
                    Rule("R", "D", self.state)
                ])
            ], limit=towers),
            Node("Markov", [
                # drop walls down from edge of roof
                Rule("DB/BB", "DB/DB", self.state, symmetry="14", rtype="all"),
                # colour inside corners
                Rule("DD/DB", "DD/DA", self.state, symmetry="14", rtype="all"),
                # flood fill inside
                Rule("AB", "AA", self.state, symmetry="1347", rtype="all"),
                # turn remaining outside black to blue sky
                Rule("B", "U", self.state, rtype="prl")
            ])
        ]

@profile
def main():
    city = City(50, 50)
    city.program_loop()

if __name__ == "__main__":
    main()