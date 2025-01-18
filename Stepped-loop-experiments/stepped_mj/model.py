from stepped_mj.mj import MarkovJunior
from stepped_mj.display import Display

def model(program, initial_dict_func=None, initial_grid_func=None, grid_height=20, grid_width=20, window_height=500, window_width=500, ticks=0):
    '''
    Construct and run a markov junior model given a program and setup

    program: list of (nested) Node and Rule objects
    initial_dict_func: function that returns initial colour dict given grid_height and grid_width inputs
    initial_grid_func: function that returns initial colour grid given grid_height and grid_width inputs
    grid_height: pixel height of program grid
    grid_width: pixel width of program grid
    window_height: pixel height of display window
    window_width: pixel width of display window
    '''

    # construct initial state
    if initial_dict_func:
        initial_dict = initial_dict_func(grid_height, grid_width)
    else:
        initial_dict = None
    if initial_grid_func:
        initial_grid = initial_grid_func(grid_height, grid_width)
    else:
        initial_grid = None

    # initialize mj
    mj = MarkovJunior(
        grid_height,
        grid_width,
        program,
        initial_grid,
        initial_dict
    )

    # initialize display
    display = Display(
        window_height,
        window_width,
        grid_height,
        grid_width,
        ticks
    )

    # draw intial state
    display.draw_setup(mj.state)

    # manual start
    display.automatic = False

    # running info
    changed_indices = []

    # loop
    while display.running:

        # handle events
        display.event_handler()

        # only step if program still running
        if mj.running:

            # automatic
            if display.automatic:

                # step
                changed_indices = mj.next()
            
            # manual
            else:

                # check action
                if display.action:
                
                    # step
                    changed_indices = mj.next()

                    # reset action
                    display.action = False

            # draw changes
            if changed_indices:

                display.draw(mj.state, changed_indices)