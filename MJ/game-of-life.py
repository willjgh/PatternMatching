from mj import *

class GameOfLife(MarkovJunior):

    def __init__(self, i, j, window_width=700, window_height=700, ticks=0):
        super().__init__(i, j, window_width=window_width, window_height=window_height, ticks=ticks) 

    def program_setup(self):

        # initial state
        for i in range(self.i):
            for j in range(self.j):

                # random black and white
                col = np.random.choice(["W", "B"])
                self.state['grid'][i, j] = col
                self.state['dict'][col].append((i, j))

        # densities

        # rule constructor function
        def rule_constructor(cell_1, cell_2, cell_3, cell_4, output_col):
            '''Given colours of 4 surrounding cells and output, construct rule'''
            if output_col == "B":
                input_col = "W"
            else:
                input_col = "B"
            input_pattern = f'*{cell_1}*/{cell_2}{input_col}{cell_3}/*{cell_3}*'
            output_pattern = f'*{cell_1}*/{cell_2}{output_col}{cell_3}/*{cell_3}*'
            return Rule(input_pattern, output_pattern, self.state, rtype="prl")

        rules = []
        input_patterns = [
            ('W', 'W', 'W', 'W'),
            ('B', 'W', 'W', 'W'),
            ('B', 'B', 'W', 'W'),
            ('B', 'W', 'B', 'W'),
            ('B', 'B', 'B', 'W'),
            ('B', 'B', 'B', 'B')
        ]
        output_cols = [
            'W',
            'B',
            'B',
            'W',
            'W',
            'B'
        ]

        for i in range(6):
            cell_1, cell_2, cell_3, cell_4 = input_patterns[i]
            output_col = output_cols[i]
            rules.append(rule_constructor(cell_1, cell_2, cell_3, cell_4, output_col))

        # program
        self.program = [
            # randomly apply given cellular rules
            Node('Random', rules)
        ]

def main():
    gameoflife = GameOfLife(50, 50, window_width=700, window_height=700, ticks=2)
    gameoflife.program_loop()

if __name__ == "__main__":
    main()