from mj import *

class RandomRules(MarkovJunior):

    def __init__(self, i, j):
        super().__init__(i, j)

    def program_setup(self):

        # initial state
        for i in range(self.i):
            for j in range(self.j):
                self.state['grid'][i, j] = 'B'
                self.state['dict']['B'].append((i, j))

        # densities

        # helper function
        def gridString(size, letter):
            row = ''.join([letter for i in range(size)])
            pattern = '/'.join([row for i in range(size)])
            return pattern

        # rule list
        rule_list = []
        alphabet = ['B', 'I', 'P', 'E', 'N', 'D', 'A', 'W', 'R', 'O', 'Y', 'G', 'U', 'S', 'K', 'F', '*']
        for letter_1 in alphabet:
            for letter_2 in alphabet:
                if (letter_1 == letter_2) or (letter_2 == '*'):
                    continue
                for size in range(2, 6):
                    rule_list.append(
                        Rule(gridString(size, letter_1), gridString(size, letter_2), self.state)
                    )
                
        # program
        self.program = [
            Node("Random", rule_list)
        ]

@profile
def main():
    randomrules = RandomRules(20, 20)
    randomrules.program_loop()

if __name__ == "__main__":
    main()