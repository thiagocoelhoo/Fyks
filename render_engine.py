import math

import pygame
import pygame.gfxdraw


def rot(x, y, ang):
    return (x*math.cos(ang) - y*math.sin(ang), y*math.cos(ang) + x*math.sin(ang))


def get_ang(w, h):
    if not w:
        ang = math.pi / 2 if h > 0 else 3 * math.pi / 2
    else:
        cos = w / (w**2 + h**2)**0.5
        sin = h / (w**2 + h**2)**0.5
        
        arccos = math.acos(cos)
        arcsin = math.asin(sin)

        if arcsin > 0:
            ang = arccos
        else:
            if arccos < 0:
                ang = arcsin
            else:
                ang = math.pi*2 - arccos
    
    return ang


def draw_vector(surface, pos, size, ang, color):
    local_pos = rot(size, 0, ang)
    end_pos = local_pos[0] + pos[0], local_pos[1] + pos[1]
    
    local_l_line = rot(size - 10, -5, ang)
    l_line = local_l_line[0] + pos[0], local_l_line[1] + pos[1]

    local_r_line = rot(size - 10, 5, ang)
    r_line = local_r_line[0] + pos[0], local_r_line[1] + pos[1]
    
    pygame.draw.aaline(surface, color, pos, end_pos)
    pygame.draw.aaline(surface, color, end_pos, l_line)
    pygame.draw.aaline(surface, color, end_pos, r_line)


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
