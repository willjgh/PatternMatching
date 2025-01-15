from mj import MarkovJunior
from node import Node
from rule import Rule
from display import Display

# define a program
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
            Node("Sequential", [
                Node("Sequential", [
                    Rule("B", "W", self.state)
                ]),
                Node("Sequential", [
                    Rule("W", "B", self.state)
                ])
            ])
        ]

def main():

    # size
    i, j= 50, 50
    winh, winw = 500, 500

    # initialize program
    fill = Fill(i, j)
    fill.program_setup()

    # initialize a display
    display = Display(window_height=winh, window_width=winw, canvas_height=i, canvas_width=j)

    # draw intial grid
    display.draw_setup(fill.state)

    program_status = True

    # loop
    while display.running:

        # handle events
        display.event_handler()

        # step program
        if program_status:# and display.action:
            changed_indices, program_status = fill.next()
            display.action = False

            # draw changes
            if changed_indices:

                display.draw(fill.state, changed_indices)

if __name__ == "__main__":
    main()