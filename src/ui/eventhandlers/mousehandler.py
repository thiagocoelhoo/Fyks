import time


class CustomMouseHandler:
    def __init__(self):
        self._moved = False
        self._pressed = False
        self._last_pressed_button = None
        self._update = None
        self.x = 0
        self.y = 0
    
    def on_mouse_release(self, x, y, button, modifiers):
        if self._update is not None:
            dt = time.time() - self._update
            if dt < 0.4:
                self.on_double_click(x, y, button, modifiers)
        self._update = time.time()

    def on_mouse_motion(self, x, y, dx, dy):
        self.x = x
        self.y = y

    def on_double_click(self, x, y, button, modifiers):
        pass
