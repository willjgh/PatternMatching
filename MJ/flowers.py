from mj import *

class Flowers(MarkovJunior):

    def __init__(self, i, j, window_width=700, window_height=700):
        super().__init__(i, j, window_width=window_width, window_height=window_height)

    def program_setup(self):

        # initial state
        for i in range(self.i):
            for j in range(self.j):
                if i == self.i - 4:
                    # 4th row from bottom green
                    self.state['grid'][i, j] = 'G'
                    self.state['dict']['G'].append((i, j))
                elif i > self.i - 4:
                    # below 4th row from bottom brown
                    self.state['grid'][i, j] = 'N'
                    self.state['dict']['N'].append((i, j))
                else:
                    # else blue
                    self.state['grid'][i, j] = 'U'
                    self.state['dict']['U'].append((i, j))

        # program
        self.program = [
            Node("Limit", [
                    Rule("UUUUU/UUUUU/UUUUU/GGGGG/NNNNN", "UUUUU/UUPUU/UUEUU/GGEGG/NNENN", self.state)
            ],limit=1),
            Node("Sequential", [
                Rule("UUU/UUU/UPU", "UUU/UPU/UEU", self.state),
                Rule("UUU/UUU/UUU/PUU/**U", "UUU/UPU/UEU/EEU/**U", self.state, symmetry="14"),
                Rule("UUUUU/UUUUU/UUUUU/UUPUU/U***U", "UUUUU/UPUPU/UEUEU/UEEEU/U***U", self.state),
                Rule("UUU/UPU/UEU/UEU", "UYU/YEY/UYU/UEU", self.state),
                Rule("UUUUU/UUUUU/UUUUU/GGGGG/NNNNN", "UUUUU/UUPUU/UUEUU/GGEGG/NNENN", self.state)
            ]),
            Node("Markov", [
                Rule("***/*P*/***", "*Y*/YEY/*Y*", self.state)
            ])
        ]

@profile
def main():
    flowers = Flowers(40, 40)
    flowers.program_loop()

if __name__ == "__main__":
    main()