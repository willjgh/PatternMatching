from mj import *

class NestedGrowth(MarkovJunior):

    def __init__(self, i, j):
        super().__init__(i, j)

    def program_setup(self):

        # initial state
        for i in range(self.i):
            for j in range(self.j):

                if (i == self.i // 2) and (j == self.j // 2):
                    self.state['grid'][i, j] = 'W'
                    self.state['dict']['W'].append((i, j))
                
                else:
                    self.state['grid'][i, j] = 'B'
                    self.state['dict']['B'].append((i, j))

        # densities

        # helper function
        def star(a, b):
            return f"*{a}{a}{a}*/{a}{a}{a}{a}{a}/{a}{a}{b}{a}{a}/{a}{a}{a}{a}{a}/*{a}{a}{a}*"
            #return f"{a}{a}{a}{a}{a}/{a}{a}{a}{a}{a}/{a}{a}{b}{a}{a}/{a}{a}{a}{a}{a}/{a}{a}{a}{a}{a}"


        # program
        self.program = [
            Node("Sequential", [
                Rule("WB", "WW", self.state, rtype="all"),
                Rule("AW", "AA", self.state, rtype="all"),
                Rule("DA", "DD", self.state, rtype="all"),
                Rule("WD", "WW", self.state, rtype="all"),
                Rule(star("W","W"), star("W","A"), self.state, rtype="all"),
                Rule(star("A","A"), star("A","D"), self.state, rtype="all"),
                Rule(star("D","D"), star("D","W"), self.state, rtype="all")
            ])
        ]  

@profile
def main():
    nestedgrowth = NestedGrowth(20, 20)
    nestedgrowth.program_loop()

if __name__ == "__main__":
    main()