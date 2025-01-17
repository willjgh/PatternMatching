import pygame
import pygame.gfxdraw

colours = {
    "B": (0  , 0  , 0  ),
    "I": (0  , 76 , 153),
    "P": (127, 0  , 255),
    "E": (0  , 153, 76 ),
    "N": (153, 76 , 0  ),
    "D": (96 , 96 , 96 ),
    "A": (192, 192, 192),
    "W": (255, 255, 255),
    "R": (255, 0  , 0  ),
    "O": (255, 165, 0  ),
    "Y": (255, 255, 0  ),
    "G": (0  , 255, 0  ),
    "U": (0  , 255, 255),
    "S": (153, 153, 255),
    "K": (255, 51 , 255),
    "F": (255, 204, 153)
}

class MultiDisplay():
    def __init__(self, window_height=700, window_width=700, canvas_height=4, canvas_width=4, multi_height=2, multi_width=2, ticks=0):

        # initialize pygame
        pygame.init()

        # window: high resolution, display on screen
        self.window_height = window_height
        self.window_width = window_width
        self.window = pygame.display.set_mode((window_width, window_height))

        # canvas: low resolution, draw on then draw to window
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width

        # grid of multiple canvases
        self.multi_height = multi_height
        self.multi_width = multi_width
        self.canvas_list = [[pygame.Surface((canvas_width, canvas_height)) for j in range(multi_width)] for i in range(multi_height)]

        # pygame settings
        pygame.display.set_caption("MarkovJunior")
        self.clock = pygame.time.Clock()
        self.ticks = ticks
        self.font = pygame.font.SysFont("Arial", 18, bold=True)

        # running flag
        self.running = True

        # action
        self.action = False
    

    def framerate_counter(self):
        '''Calculate and display frames per second'''

        # get framerate
        fps = str(int(self.clock.get_fps()))

        # create text
        fps_text = self.font.render(fps, 1, (0, 255, 0))

        # display on window: top left
        self.window.blit(fps_text, (0, 0))

    
    def event_handler(self):
        '''Handle inputs'''

        # loop over events
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        # quit
        if not self.running:
            pygame.quit()

    def draw_setup(self, program_list):
        '''Draw initial grid to each canvas '''

        # loop over each canvas
        for i in range(self.multi_height):
            for j in range(self.multi_width):

                # get associated state
                state = program_list[i][j].state

                # loop over each letter
                for letter, indices in state['dict'].items():

                    # get colour
                    colour = colours[letter]

                    # draw each pixel
                    for idx in indices:
                        pygame.gfxdraw.pixel(self.canvas_list[i][j], idx[1], idx[0], colour)
                
                # blit canvas to window
                self.window.blit(
                    pygame.transform.scale(
                        self.canvas_list[i][j],
                        (
                            self.window_width // self.multi_width - 1,
                            self.window_height // self.multi_height - 1
                        )
                    ),
                    (
                        j * (self.window_width // self.multi_width),
                        i * (self.window_height // self.multi_height)
                    )
                )
        
        # update display
        pygame.display.flip()

    def draw(self, program_list, indices_list):
        '''Draw changes indices to each canvas'''

        # limit speed
        self.clock.tick(self.ticks)

        # loop over each canvas
        for i in range(self.multi_height):
            for j in range(self.multi_width):

                # if program finished: skip
                if not program_list[i][j].running:
                    continue
                
                # get associated state
                state = program_list[i][j].state

                # get associated indices
                indices = indices_list[i][j]

                # if empty: skip
                if not indices:
                    continue

                # loop over changed indices
                for idx in indices:

                    # get colour
                    colour = colours[state['grid'][*idx]]

                    # draw
                    pygame.gfxdraw.pixel(self.canvas_list[i][j], idx[1], idx[0], colour)

                # blit canvas to window
                self.window.blit(
                    pygame.transform.scale(
                        self.canvas_list[i][j],
                        (
                            self.window_width // self.multi_width - 1,
                            self.window_height // self.multi_height - 1
                        )
                    ),
                    (
                        j * (self.window_width // self.multi_width),
                        i * (self.window_height // self.multi_height)
                    )
                )

        # update display
        pygame.display.flip()