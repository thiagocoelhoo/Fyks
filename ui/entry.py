import weakref
import string

import pygame
# from PIL import ImageFont

from .widget import Widget
from .label import Label
from render_engine import aa_round_rect, _aa_render_region
import core


printset = set(string.printable)
mouse = core.get_mouse()
eventhandler = core.get_eventhandler()

# font = ImageFont.truetype('times.ttf', 12)
# size = font.getsize('Hello world')


class Entry(Widget):
    __instances = set()

    def __init__(self, name, position, size, text=''):
        super().__init__(position, size)
        text_pos = (position[0] + 4, position[1] + 6)

        self.cursor = len(text)
        self.label = Label(name, (position[0], position[1]-20))
        self.label.color = (80, 80, 80)
        self.content_label = Label('', text_pos)

        self.content_label.color = (50, 50, 50)
        self.activated_color = (100, 100, 255)
        self.none_color = (150, 150, 150)
        self.color = self.none_color

        self.text = text
        self.active = False
        self.limit = self.size[0] // 8 - 1

        self.__instances.add(weakref.ref(self))

        eventhandler.add_handler(pygame.KEYDOWN, self.on_keydown)
        eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousebuttondown)

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

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value
        self.content_label.text = self.text

    def on_keydown(self, key):
        if self.active:
            if key.key == pygame.K_BACKSPACE:
                if self.cursor > 0:
                    self.text = self.text[:self.cursor - 1] + self.text[self.cursor:]
                    self.cursor -= 1
            elif key.key == pygame.K_RETURN:
                self.active = False
            elif key.key == pygame.K_LEFT and self.cursor > 0:
                self.cursor -= 1
            elif key.key == pygame.K_RIGHT:
                if self.cursor < len(self.text):
                    self.cursor += 1
            else:
                uc = key.unicode
                print("UC:", uc)
                self.text = self.text[:self.cursor] + uc + self.text[self.cursor:]
                self.cursor += 1
                
    def on_mousebuttondown(self, event):
        if event.button == 1:
            if self.is_mouse_over():
                self.active = True
            else:
                self.active = False

    def update(self, dt, event=pygame.NOEVENT):
        if mouse.pressed[0]:
            if self.is_mouse_over():
                self.active = True
                self.color = self.activated_color
            else:
                self.active = False
                self.color = self.none_color

    def draw(self, surface):
        aa_round_rect(surface, (self.pos, self.size), self.color, rad=2, border=1, inside=(240, 240, 240))

        if self.active:
            font_x = self.x + 4
            font_y = self.y + 4
            if self.cursor > self.limit:
                cpos = self.limit
            else:
                cpos = self.cursor
            pygame.draw.rect(surface, (0, 0, 0), ((font_x + 8 * cpos, font_y), (2, 16)))
        
        self.label.draw(surface)
        self.content_label.draw(surface, limit=self.limit)
