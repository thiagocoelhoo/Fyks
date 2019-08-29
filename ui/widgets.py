import weakref

import pygame
import pygame.gfxdraw
import numpy as np

from .widget import Widget
from .label import Label
from .button import Button
from render_engine import aa_round_rect, _aa_render_region
import core

mouse = core.get_mouse()


class Entry(Widget):
    __instances = set()

    def __init__(self, name, position, size):
        super().__init__(position, size)
        text_pos = (position[0] + 4, position[1] + 4)
        self.cursor = 0
        self.label = Label(name, (position[0], position[1]-20))
        self.label.color = (80, 80, 80)
        self.content_label = Label('', text_pos)
        self.content_label.color = (50, 50, 50)
        self.activated_color = (100, 100, 255)    # (80, 80, 80)
        self.none_color = (150, 150, 150)
        self.color = self.none_color
        self.text = ''
        self.active = False
        self.__instances.add(weakref.ref(self))

    @classmethod
    def all(cls):
        dead = set()
        for ref in cls.__instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls.__instances -= dead

    def on_keydown(self, key):
        if key.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif key.key == pygame.K_RETURN:
            self.active = False
        else:
            self.text = self.text + key.unicode
        self.content_label.text = self.text

    def update(self, dt, event=pygame.NOEVENT):
        if mouse.pressed[0]:
            if self.is_hover():
                self.active = True
                self.color = self.activated_color
            else:
                self.active = False
                self.color = self.none_color

    def draw(self, surface):
        # rect = pygame.Rect((self.pos, self.size))
        # pygame.gfxdraw.box(surface, rect, (240, 240, 240))
        # super().draw(surface)
        aa_round_rect(surface, (self.pos, self.size), self.color, rad=2, border=1, inside=(240, 240, 240))
        
        self.label.draw(surface)
        self.content_label.draw(surface)


class IntEntry(Entry):
    pass


class Frame(Widget):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.color = (0, 0, 0)
        self.bg_color = (10, 10, 10)
        # self.w, self.h = size
        self.surface = pygame.surface.Surface(size)
        self.widgets = dict()
        self.autoclear = True
    
    def __setitem__(self, name, widget):
        self.add_widget(name, widget)
    
    def add_widget(self, name, widget):
        widget.master = self
        self.widgets[name] = widget

    def draw(self, surface):
        if self.autoclear:
            self.surface.fill(self.bg_color)
        
        for wid in self.widgets.values():
            wid.draw(self.surface)
        surface.blit(self.surface, self.pos)
        super().draw(surface)

    def update(self, dt):
        for wid in self.widgets.values():
            wid.update(dt)


class SubWindow(Frame):
    def __init__(self, position, width, height):
        super().__init__(position, (width, height + 30))
        self.surface = pygame.Surface((width, height + 30))
        self.moving = False
        self.autoclear = False
        self.color = (0, 255, 0)

    def hover_controler_bar(self, x, y):
        gx, gy = self.global_pos
        if gx <= x <= gx + self.w:
            if gy <= y <= gy + 30:
                return True
        return False
    
    def update(self, dt):
        super().update(dt)
        mx, my = mouse.pos
        rx, ry = mouse.rel
        
        if self.moving:
            self.pos[0] += rx
            self.pos[1] += ry
        elif self.hover_controler_bar(mx, my) and mouse.pressed[0]:
            self.moving = True
        
        if not mouse.pressed[0] and self.moving:
            self.moving = False
    
    def draw(self, surface):
        pygame.draw.line(self.surface, (0, 255, 0), (0, 30), (self.w, 30))
        
        surface.blit(self.surface, self.pos)
        super().draw(surface)


class Graphic(Widget):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.surface = pygame.surface.Surface(size)
        self.color = (100, 100, 100)
        self.points = []

    def plot(self, x, y):
        self.points = list(zip(x, y))    
    
    def draw_grid(self):
        color = (10, 10, 10)
        cols = self.w / 10
        rows = self.h / 10

        for c in range(int(cols)):
            x1 = int((c * self.w / cols - self.x) % self.w )
            y1 = 0
            y2 = self.h
            pygame.gfxdraw.vline(self.surface, x1, y1, y2, color)
    
        for r in range(int(rows)):
            x1 = 0
            x2 = self.w
            y1 = (int(r * self.h / rows) - self.y) % self.h
            pygame.gfxdraw.hline(self.surface, x1, x2, y1, color)
        
        pygame.gfxdraw.line(self.surface, self.w//2, 0, self.w//2, self.h, (50, 255, 50))
        pygame.gfxdraw.line(self.surface, 0, self.h//2, self.w, self.h//2, (255, 50, 50))
    
    def draw(self, surface):
        self.surface.fill((20, 20, 20))
        self.draw_grid()
        if len(self.points) > 1:
            pygame.draw.lines(self.surface, (60, 80, 240), False, self.points)
        
        surface.blit(self.surface, self.pos)
        super().draw(surface)


class GraphicFrame(Frame):
    def __init__(self, position, size, graphic_size=(200, 200)):
        # super().__init__(position, size[0], size[1])
        super().__init__(position, size)
        self.graphic = Graphic((4, 4), graphic_size)
        self.autoclear = False
        self.add_widget('simple_button_one', Button((212, 8), (160, 25), 'Simple Button one'))
        self.add_widget('simple_button_two', Button((212, 40), (160, 25), 'Simple Button two'))
        self.add_widget('simple_button_three', Button((212, 73), (160, 25), 'Simple Button three'))
    
    def plot(self, x, y):
        self.graphic.plot(x, y)
    
    def update(self, dt):
        super().update(dt)
        self.graphic.update(dt)

    def draw(self, surface):
        self.surface.fill((220, 220, 220))
        self.graphic.draw(self.surface)

        for wid in self.widgets.values():
            wid.draw(self.surface)
        surface.blit(self.surface, self.pos)
        super().draw(surface)


class SplitedFrame(Frame):
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class ScroolingBar(Widget):
    pass
