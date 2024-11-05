from mj import *

class River(MarkovJunior):

    def __init__(self, i, j):
        super().__init__(i, j)

    def program_setup(self):

        # initial state
        for i in range(self.i):
            for j in range(self.j):
                self.state['grid'][i, j] = 'B'
                self.state['dict']['B'].append((i, j))

        # densities

        # program
        self.program = [
            # voroni seeds
            Node("Limit", [
                Rule("B", "W", self.state),
                Rule("B", "R", self.state),
            ], limit=3),
            # expand voroni
            Node("Sequential", [
                Rule("WB", "WW", self.state),
                Rule("RB", "RR", self.state)
            ]),
            # middle to river
            Node("Markov", [
                Rule("RW", "UU", self.state, rtype="prl")
            ]),
            # rest to black
            Node("Sequential", [
                Rule("W", "B", self.state, rtype="prl"),
                Rule("R", "B", self.state, rtype="prl")
            ]),
            # yellow border
            Node("Markov", [
                Rule("UB", "UY", self.state)
            ]),
            # yellow to blue
            Node("Markov", [
                Rule("Y", "U", self.state, rtype="prl")
            ]),
            # light green border
            Node("Markov", [
                Rule("UB", "UG", self.state)
            ]),
            # spawn dark green seeds
            Node("Limit", [
                Rule("B", "E", self.state)
            ], limit=13),
            # grow greens
            Node("Sequential", [
                Rule("GB", "GG", self.state),
                Rule("EB", "EE", self.state)
            ])
        ]

@profile
def main():
    river = River(50, 50)
    river.program_loop()

if __name__ == "__main__":
    main()