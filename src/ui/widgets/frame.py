from pyglet import gl

from ui import widgets, elements
import graphicutils as gu


class Frame(widgets.Widget, elements.Frame):
    def __init__(self, x, y, w, h, parent=None):
        super().__init__(x, y, w, h, parent)
        self.color = (0.9, 0.9, 0.9, 1)
        self.border_color = (0, 0, 0, 0)
        self.border_radius = 0
        self.elements = []

    def toggle_is_visible(self):
        self.is_visible = not self.is_visible
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.hover:
            for widget in self.elements:
                if widget.is_visible:
                    widget.on_mouse_scroll(
                        x=x, y=y, 
                        scroll_x=scroll_x,
                        scroll_y=scroll_y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for widget in self.elements:
            if widget.is_visible:
                widget.on_mouse_drag(
                    x=x, y=y,
                    dx=dx, dy=dy,
                    buttons=buttons,
                    modifiers=modifiers
                )

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.elements:
            if widget.is_visible:
                widget.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        pos_on_screen = self.global_position

        if self.hover:
            hover_widget = None
            for widget in self.elements:
                if widget.is_visible:
                    if widget.is_hover(x, y):
                        hover_widget = widget
                        self.pressed = False
                    else:
                        widget.pressed = False
            
            if not self.pressed:
                hover_widget.on_mouse_press(
                    x=x, y=y,
                    button=button, 
                    modifiers=modifiers)
    
    def on_mouse_release(self, x, y, button, modifiers):
        for widget in self.elements:
            if widget.is_visible:
                widget.on_mouse_release(x, y, button, modifiers)
    
    def on_key_press(self, symbol, modifiers):
        for widget in self.elements:
            if widget.is_visible:
                widget.on_key_press(symbol, modifiers)

    def update(self, dt):
        for widget in self.elements:
            if widget.is_visible:
                widget.update(dt)

    def draw_widgets(self, offset_x, offset_y):
        for widget in self.elements:
            if widget.is_visible:
                widget.draw(offset_x, offset_y)

    def draw(self, offset_x=0, offset_y=0):
        x = self.x + offset_x
        y = self.y + offset_y
        gl.glColor4f(*self.color)
        gu.draw_rounded_rect(
            x, y,
            self.width,
            self.height,
            self.border_radius,
            gl.GL_POLYGON
        )
        gl.glColor4f(*self.border_color)
        gu.draw_rounded_rect(
            x, y,
            self.width,
            self.height,
            self.border_radius,
            gl.GL_LINE_LOOP)
        self.draw_widgets(x, y)
