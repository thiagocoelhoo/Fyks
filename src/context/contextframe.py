import pickle

from pyglet.window import mouse, key

from ui import Frame, Button, CustomMouseHandler
from context.context import Context
from context.context_widgets import (
    ContextOptionsMenu,
    ToolBox,
    RigidbodyInfoWindow
)


class ContextFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = Context(0, 0, self.w, self.h)
        self.mouse_handler = CustomMouseHandler()
        self.mouse_handler.on_double_click = self.on_double_click
        self.running = True

        self.build()

        self.KEYMAP = {
            (key.MOD_SHIFT, key.A): 'options',
            (0, key.HOME): 'home',
            (0, key.DELETE): 'delete',
            (0, key.SPACE): 'pause',
        }
    
    def build(self):
        self.toolbox = ToolBox(self)
        self.opt = ContextOptionsMenu(self)
        self.rbinfo = RigidbodyInfoWindow(self)
    
    def show_options(self):
        opt = self.opt
        opt.x = self.mouse_handler.x
        opt.y = self.mouse_handler.y - opt.h
        opt.display = True

    def pause(self):
        self.running = not self.running

    def save(self):
        with open('context.fyks', 'wb') as f:
            pickle.dump(self.context, f)

    def load(self):
        with open('context.fyks', 'rb') as f:
            ctx = pickle.load(f)
            self.context = ctx

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.activated == 1:
            if scroll_y < 0:
                if self.context.camera.zoom > 0.05:
                    self.context.camera.zoom -= 0.05
            elif scroll_y > 0:
                self.context.camera.zoom += 0.05
    
    def on_mouse_press(self, x, y, button, modifiers): 
        super().on_mouse_press(x, y, button, modifiers)
        if self.activated == 1:
            if button == mouse.RIGHT:
                self.context.selection = [x, y, x, y]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        if self.activated == 1:
            if buttons == mouse.LEFT:
                self.context.camera.x -= dx
                self.context.camera.y -= dy
            elif buttons == mouse.RIGHT:
                if self.context.selection is not None:
                    self.context.selection[2] = x
                    self.context.selection[3] = y

    def on_mouse_release(self, x, y, button, modifiers):
        super().on_mouse_release(x, y, button, modifiers)
        self.mouse_handler.on_mouse_release(x, y, button, modifiers)
        if button == mouse.RIGHT:
            self.context.select()
            self.context.selection = None
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_handler.on_mouse_motion(x, y, dx, dy)
    
    def on_double_click(self, x, y, button, modifiers):
        self.context.select_closer(x, y)
        if self.context.selected:
            self.rbinfo.x = x
            self.rbinfo.y = y
            self.rbinfo.display = True
    
    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        command = self.KEYMAP.get((modifiers, symbol))
        
        if command == 'options':
            self.show_options()
        elif command == 'home':
            self.context.camera.to_home()
        elif command == 'delete':
            self.context.delete_selected()
        elif command == 'pause':
            self.pause()
        
    def draw(self, offset_x=0, offset_y=0):
        self.context.draw()
        self.draw_content(offset_x, offset_y)

    def update(self, dt):
        if self.running:
            self.context.update(dt)
