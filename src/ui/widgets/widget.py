from ui import elements


class Widget(elements.Element):
    def __init__(self, x, y, w, h, parent=None):
        super().__init__(x, y, w, h, parent)
        self.pressed = False
        self.hover = False
        self.is_visible = True
        self.border_radius = 4
        self.background_color = (0, 0, 0, 1)

    def is_hover(self, x, y):
        return (self.x < x < self.x + self.width and self.y < y < self.y + self.height)

    def on_resize(self, w, h):
        self.resize(w, h)
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        self.hover = self.is_hover(x, y)
        self.pressed = self.hover

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def draw(self, offset_x=0, offset_y=0):
        pass

    def update(self, dt):
        pass
