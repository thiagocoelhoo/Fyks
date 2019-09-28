import pygame
import pygame.gfxdraw

import core


class App:
    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.mouse = core.get_mouse()
        self.views = {}
        self.current_view = None
        self.running = False
        self.dt = 0

        self.eventhandler = core.get_eventhandler()
        self.eventhandler.add_handler(pygame.QUIT, self.on_quit)

    def on_quit(self, event):
        self.running = False
    
    def run(self):
        self.running = True
        while self.running:
            self.eventhandler.update()
            self.mouse.update()
            
            self.views[self.current_view].update(self.dt)
            self.views[self.current_view].draw(self.surface)  

            pygame.display.update()
            self.dt = self.clock.tick(0) / 1000
        
        pygame.quit()
