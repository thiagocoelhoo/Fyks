from ui import widgets


class Layer(widgets.Layout):
    def is_hover(self, x, y):
        for widget in self.elements:
            if widget.is_visible and widget.is_hover(x, y):
                return True
        return False

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
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
                    modifiers=modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.elements:
            if widget.is_visible:
                widget.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.elements:
            if widget.is_visible:
                if widget.is_hover(x, y):
                    widget.on_mouse_press(x, y, button, modifiers)
    
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

    def draw_widgets(self):
        for widget in sorted(self.elements, key=lambda i: i.z_index):
            if widget.is_visible:
                widget.draw()

    def draw(self):
        self.update_viewport()
        self.draw_widgets()
