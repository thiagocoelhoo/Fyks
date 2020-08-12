from ui.widget import Widget
import core

import random


class Frame(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = (0.9, 0.9, 0.9, 1)
        self.content = []

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
        over = super().on_mouse_press(x, y, button, modifiers)
        if over:
            for widget in self.content:
                if widget.display:
                    widget_over = widget.on_mouse_press(
                        x=x - self.x,
                        y=y - self.y,
                        button=button,
                        modifiers=modifiers
                    )
                    if widget_over:
                        self.activated = False
        return over
    
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
            if widget.display:
                widget.update(dt)

    def draw_content(self, offset_x, offset_y):
        for widget in self.content:
            if widget.display:
                widget.draw(
                    offset_x=offset_x + self.x,
                    offset_y=offset_y + self.y
                )

    def draw(self, offset_x=0, offset_y=0):
        self.fill_background(self.color)
        self.draw_content(offset_x, offset_y)
