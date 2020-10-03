from pyglet import gl

from ui import Widget
import graphicutils as gu


class Frame(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = (0.9, 0.9, 0.9, 1)
        self.border_color = (0.7, 0.7, 0.7, 1)
        self.border_radius = 0
        self.children = []

    def toggle_is_visible(self):
        self.is_visible = not self.is_visible
    
    def on_resize(self, w, h):
        for widget in self.children:
            widget.on_resize(w, h)
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.hover:
            for widget in self.children:
                if widget.is_visible:
                    widget.on_mouse_scroll(
                        x=x - self.x,
                        y=y - self.y,
                        scroll_x=scroll_x,
                        scroll_y=scroll_y
                    )

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for widget in self.children:
            if widget.is_visible:
                widget.on_mouse_drag(
                    x=x - self.x,
                    y=y - self.y,
                    dx=dx,
                    dy=dy,
                    buttons=buttons,
                    modifiers=modifiers
                )

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.children:
            if widget.is_visible:
                widget.on_mouse_motion(x, y, dx, dy)

    def on_mouse_release(self, x, y, button, modifiers):
        for widget in self.children:
            if widget.is_visible:
                widget.on_mouse_release(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        for widget in self.children:
            if widget.is_visible:
                widget.on_key_press(symbol, modifiers)

    def update(self, dt):
        for widget in self.children:
            if widget.is_visible:
                widget.update(dt)

    def draw_children(self, offset_x, offset_y):
        for widget in self.children:
            if widget.is_visible:
                widget.draw(
                    offset_x=offset_x + self.x,
                    offset_y=offset_y + self.y
                )

    def draw(self, offset_x=0, offset_y=0):
        gl.glColor4f(*self.color)
        gu.draw_rounded_rect(
            self.x + offset_x,
            self.y + offset_y,
            self.w, self.h,
            self.border_radius,
            gl.GL_POLYGON
        )
        gl.glColor4f(*self.border_color)
        gu.draw_rounded_rect(
            self.x + offset_x,
            self.y + offset_y,
            self.w, self.h,
            self.border_radius,
            gl.GL_LINE_LOOP
        )
        self.draw_children(offset_x, offset_y)
