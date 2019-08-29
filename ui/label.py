import pygame

from .widget import Widget


class Label(Widget):
    pygame.font.init()

    def __init__(self, text, position):
        super().__init__(position, (0, 0), False)
        self.font = pygame.font.SysFont('consolas', 14)
        self.text = text
        self.color = (255, 255, 255)
    
    def draw(self, surface):
        rendered_text = self.font.render(self.text, True, self.color)
        surface.blit(rendered_text, self.pos)
