import pygame
import pygame.gfxdraw

from .widget import Widget
from .label import Label
from .button import Button
from .frame import Frame
from .entry import Entry
from render_engine import aa_round_rect, _aa_render_region
import core

mouse = core.get_mouse()
eventhandler = core.get_eventhandler()


class SubWindow(Frame):
    def __init__(self, position, width, height, title='-', resizable=True):
        super().__init__(position, (width, height + 30))
        self.surface = pygame.Surface((width, height + 30))
        self.resizable = resizable
        self.autoclear = False
        self.active = False
        self.moving = False
        self.mode = "null"
        self.rel = [0, 0]
        
        self.color = (50, 50, 50)
        self.bar_color = core.theme["window-controller-bar"]
        
        self.title = title
        self.title_label = Label(title, (8, 8))        
        
        eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousedown)
        eventhandler.add_handler(pygame.MOUSEBUTTONUP, self.on_mouseup)
        eventhandler.add_handler(pygame.MOUSEMOTION, self.on_mousemove)

    def resize(self, width, height):
        self.surface = pygame.Surface((width, height))
        self.w = width
        self.h = height
    
    def on_mousedown(self, event):
        if event.button == 1:
            if self.is_mouse_over():
                self.active = True
                
                if self.resizable:
                    x, y = event.pos
                    if self.x + self.w - 10 <= x <= self.x + self.w and\
                        self.y + self.h - 10 <= y <= self.y + self.h:
                        self.mode = "resizing"
                
                if self.hover_controler_bar(event.pos[0], event.pos[1]):
                    self.mode = "moving"
                    self.rel = [mouse.pos[0] - self.pos[0], mouse.pos[1] - self.pos[1]]
            else:
                self.active = False

    def on_mouseup(self, event):
        if event.button == 1:
            if self.mode == "moving" or self.mode == "resizing":
                self.mode = "null"

    def on_mousemove(self, event):
        if self.mode == "moving":
            self.pos[0] = mouse.pos[0] - self.rel[0]
            self.pos[1] = mouse.pos[1] - self.rel[1]
        elif self.mode == "resizing":
            n_width = max(event.pos[0] - self.x, 100)
            n_height = max(event.pos[1] - self.y, 40)
            self.resize(n_width, n_height)

    def hover_controler_bar(self, x, y):
        gx, gy = self.global_pos
        if gx <= x <= gx + self.w:
            if gy <= y <= gy + 30:
                return True
        return False
    
    def update(self, dt):
        if self.active:
            super().update(dt)

    def draw(self, surface):
        super().draw(surface)
        pygame.draw.rect(self.surface, self.bar_color, [(0, 0), (self.w, 30)])
        pygame.draw.line(self.surface, (50, 50, 50), (0, 30), (self.w, 30))
        self.title_label.draw(self.surface)
        surface.blit(self.surface, self.pos)


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


class GraphicFrame(SubWindow):
    def __init__(self, position, size, graphic_size=(200, 200)):
        super().__init__(position, size[0], size[1])
        self.graphic = Graphic((4, 34), graphic_size)
        self.autoclear = False

        self.add_widget('simple_button_one', Button((212, 38), (160, 25), 'Simple Button one'))
        self.add_widget('simple_button_two', Button((212, 70), (160, 25), 'Simple Button two'))
        self.add_widget('simple_button_three', Button((212, 103), (160, 25), 'Simple Button three'))
    
    def plot(self, x, y):
        self.graphic.plot(x, y)
    
    def update(self, dt):
        super().update(dt)
        self.graphic.update(dt)

    def draw(self, surface):
        self.surface.fill(self.bg_color)
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
