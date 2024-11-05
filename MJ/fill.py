from mj import *

class Fill(MarkovJunior):

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
            Node(
                "Markov", [
                    Rule("B", "W", self.state)
                ]
            )
        ]

@profile
def main():
    fill = Fill(20, 20)
    fill.program_loop()

if __name__ == "__main__":
    main()