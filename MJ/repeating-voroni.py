from mj import *

class RepeatingVoroni(MarkovJunior):

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
                    Node(
                        "Sequential", [
                            Node(
                                "Limit", [
                                    Rule("B", "W", self.state)
                                ],
                                limit = 1
                            ),
                            Node(
                                "Limit", [
                                    Rule("B", "R", self.state)
                                ],
                                limit = 1
                            ),
                            Node(
                                "Sequential", [
                                    Rule("WB", "WW", self.state, rtype="one"),
                                    Rule("RB", "RR", self.state, rtype="one")
                                ]
                            )
                        ]
                    ),
                    Node(
                        "Sequential", [
                            Rule("W", "B", self.state, rtype="one"),
                            Rule("R", "B", self.state, rtype="one")
                        ]
                    )
                ]
            )
        ]

@profile
def main():
    repeatingvoroni = RepeatingVoroni(20, 20)
    repeatingvoroni.program_loop()

if __name__ == "__main__":
    main()