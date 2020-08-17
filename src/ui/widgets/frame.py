from pyglet.gl import *

from ui import Widget
from graphicutils import graphicutils


class Frame(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = (0.9, 0.9, 0.9, 1)
        self.border_color = (0.7, 0.7, 0.7, 1)
        self.border_radius = 0
        self.content = []

    def toggle_display(self):
        self.display = not self.display
        
    def add(self, widget):
        widget.x += self.padding
        widget.y += self.padding
        self.content.append(widget)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.activated:
            for widget in self.content:
                if widget.display:
                    widget_over = widget.on_mouse_scroll(
                        x=x - self.x,
                        y=y - self.y,
                        scroll_x=scroll_x,
                        scroll_y=scroll_y
                    )

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for widget in self.content:
            if widget.display:
                widget_over = widget.on_mouse_drag(
                    x=x - self.x,
                    y=y - self.y,
                    dx=dx,
                    dy=dy,
                    buttons=buttons,
                    modifiers=modifiers
                )
    
    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        if self.activated == 1 :
            for widget in self.content:
                if widget.display:
                    widget.on_mouse_press(
                        x=x - self.x,
                        y=y - self.y,
                        button=button,
                        modifiers=modifiers
                    )
                    
                    if widget.activated > 0: 
                        self.activated += 1
    
    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.content:
            widget.on_mouse_motion(x, y, dx, dy)

    def on_mouse_release(self, x, y, button, modifiers):
        for widget in self.content:
            widget.on_mouse_release(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        for widget in self.content:
            widget.on_key_press(symbol, modifiers)

    def update(self, dt):
        for widget in self.content:
            #if widget.display:
            widget.update(dt)

    def draw_content(self, offset_x, offset_y):
        for widget in self.content:
            if widget.display:
                widget.draw(
                    offset_x=offset_x + self.x,
                    offset_y=offset_y + self.y
                )

    def draw(self, offset_x=0, offset_y=0):
        glColor4f(*self.color)
        graphicutils.draw_rect(
            self.x + offset_x,
            self.y + offset_y,
            self.w, self.h,
            GL_QUADS
        )
        glColor4f(*self.border_color)
        graphicutils.draw_rect(
            self.x + offset_x,
            self.y + offset_y,
            self.w, self.h,
            GL_LINE_LOOP
        )
        self.draw_content(offset_x, offset_y)
