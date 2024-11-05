from mj import *

class FloodFill(MarkovJunior):

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
            Node("Limit", [
                    Rule("B", "W", self.state)
                ],
                limit=1
            ),
            Node(
                "Markov", [
                    Rule("WB", "WW", self.state)
                ]
            )
        ]

@profile
def main():
    floodfill = FloodFill(20, 20)
    floodfill.program_loop()

if __name__ == "__main__":
    main()