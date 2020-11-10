from pyglet.gl import *

from ui import widgets
import graphicutils as gu


class Button(widgets.Widget):
    def __init__(self, x, y, w, h, parent=None, text='Button', command=None):
        super().__init__(x, y, w, h, parent)
        self.command = command or (lambda: print('Pressed'))
        self.label = widgets.Label(8, 6, 0, 0)
        self.label.text = text
        self.pressed = False
        self.padding = 8
        
        self.null_color = (0.8, 0.8, 0.9, 1)
        self.pressed_color = (0.7, 0.7, 0.9, 1)
        self.border_color = (0.5, 0.5, 0.6, 0.8)
        self.border_radius = 6

        self.color = self.null_color
    
    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        if self.pressed:
            self.color = self.pressed_color
            
    def on_mouse_release(self, x, y, button, modifiers):
        if self.pressed:
            self.color = self.null_color
            self.pressed = False
            self.command()
    
    def draw(self, offset_x=0, offset_y=0):
        glColor4f(*self.color)
        gu.draw_rounded_rect(
            self.x + offset_x, 
            self.y + offset_y,
            self.width,
            self.height,
            self.border_radius,
            GL_POLYGON
        )

        glColor4f(*self.border_color)
        gu.draw_rounded_rect(
            self.x + offset_x, 
            self.y + offset_y,
            self.width,
            self.height,
            self.border_radius + 1, 
            GL_LINE_LOOP
        )

        self.label.draw(
            self.x + offset_x,
            self.y + offset_y
        )
