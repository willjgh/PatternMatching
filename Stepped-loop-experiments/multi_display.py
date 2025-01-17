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
    def __init__(self, window_width=700, window_height=700, canvas_width=4, canvas_height=4, ticks=0, multi_width=2, multi_height=2):

        # initialize pygame
        pygame.init()

        # window: high resolution, display on screen
        self.window_width = window_width
        self.window_height = window_height
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        # setup grid of multiple canvases

        # canvas: low resolution, draw on then draw to window
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.canvas = pygame.Surface((self.canvas_width, self.canvas_height))

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

                if event.key == pygame.K_RIGHT:
                    self.action = True

        # quit
        if not self.running:
            pygame.quit()

    def draw_setup(self, state):
        '''Draw the full initial grid'''

        # loop over each letter
        for letter, indices in state['dict'].items():

            # get colour
            colour = colours[letter]

            # draw each pixel
            for idx in indices:
                pygame.gfxdraw.pixel(self.canvas, idx[1], idx[0], colour)
        
        # blit canvas to window
        self.window.blit(pygame.transform.scale(self.canvas, self.window.get_rect().size), (0, 0))
        
        # add framerate
        #self.framerate_counter()

        # update display
        pygame.display.flip()

        # check for quit
        #self.event_handler()

    def draw(self, state, indices):
        '''Draw indices that were changed by rules as new colours'''

        # limit speed
        self.clock.tick(self.ticks)

        # loop over changed indices
        for idx in indices:

            # get colour
            colour = colours[state['grid'][*idx]]

            # draw
            pygame.gfxdraw.pixel(self.canvas, idx[1], idx[0], colour)

        # blit canvas to window
        self.window.blit(pygame.transform.scale(self.canvas, self.window.get_rect().size), (0, 0))
        
        # add framerate
        #self.framerate_counter()

        # update display
        pygame.display.flip()

        # check for quit
        #self.event_handler()