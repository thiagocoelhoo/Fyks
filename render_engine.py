import math

import pygame
import pygame.gfxdraw


def rounded_rect(w, h, r, border, color, border_color):
    surface = pygame.surface.Surface((w, h)).convert_alpha()
    surface.fill((0, 0, 0, 0))
    
    pygame.draw.rect(surface, color, [r, 0, w - 2*r, h])
    pygame.draw.rect(surface, color, [0, r, r, h - 2*r])
    pygame.draw.rect(surface, color, [w-r, r, r, h - 2*r])
    pygame.gfxdraw.filled_circle(surface, r, r, r, color)
    pygame.gfxdraw.filled_circle(surface, w-r, r, r, color)
    pygame.gfxdraw.filled_circle(surface, w-r, h-r, r, color)
    pygame.gfxdraw.filled_circle(surface, r, h-r, r, color)

    return surface


def aa_round_rect(surface, rect, color, rad=20, border=0, inside=(0,0,0)):
    rect = pygame.Rect(rect)
    _aa_render_region(surface, rect, color, rad)
    if border:
        rect.inflate_ip(-2*border, -2*border)
        _aa_render_region(surface, rect, inside, rad)


def _aa_render_region(image, rect, color, rad):
    corners = rect.inflate(-2*rad-1, -2*rad-1)
    for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
        x, y = getattr(corners, attribute)
        pygame.gfxdraw.aacircle(image, x, y, rad, color)
        pygame.gfxdraw.filled_circle(image, x, y, rad, color)
    image.fill(color, rect.inflate(-2*rad,0))
    image.fill(color, rect.inflate(0,-2*rad))
