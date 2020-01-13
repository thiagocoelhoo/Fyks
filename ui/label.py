import pygame

from .widget import Widget
import core


class Label(Widget):
    pygame.font.init()

    def __init__(self, text, position):
        super().__init__(position, (0, 0), False)
        self.font = pygame.font.SysFont('consolas', 14)
        self.text = text
        self.color = core.theme['label-color']

    def draw(self, surface, limit=0):
        if limit and len(self.text) > limit:
            text = self.text[-limit:]
        else:
            text = self.text
        
        rendered_text = self.font.render(text, True, self.color)
        surface.blit(rendered_text, self.pos)
