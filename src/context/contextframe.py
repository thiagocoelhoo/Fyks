import pyglet
from pyglet.window import mouse, key

from context.context import Context
from context.context_widgets import ContextOptionsMenu, ToolBox
from ui import Frame, Button, Entry

mx = 0
my = 0


class ContextFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = Context(0, 0, self.w, self.h)
        self.running = True
        
        self.build_options()
        
        self.KEYMAP = {
            (key.MOD_SHIFT, key.A): 'options',
            (0, key.HOME): 'home',
            (0, key.DELETE): 'delete',
            (0, key.SPACE): 'pause',
        }
    
    def build_options(self):
        self.toolbox = ToolBox(self)
        self.opt = ContextOptionsMenu(self)
    
    def show_options(self):
        opt = self.opt
        opt.x = mx
        opt.y = my - opt.h
        opt.display = True

    def pause(self):
        self.running = not self.running
    
    def on_mouse_motion(self, x, y, dx, dy):
        global mx, my
        mx = x
        my = y
        
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.activated:
            if scroll_y < 0:
                if self.context.camera.zoom > 0.05:
                    self.context.camera.zoom -= 0.05
            elif scroll_y > 0:
                self.context.camera.zoom += 0.05
    
    def on_mouse_press(self, x, y, button, modifiers): 
        super().on_mouse_press(x, y, button, modifiers)
        if self.activated:
            if button == mouse.RIGHT:
                self.context.selection = [x, y, x, y]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons == mouse.LEFT:
            self.context.camera.x -= dx
            self.context.camera.y -= dy
        elif buttons == mouse.RIGHT:
            if self.context.selection is not None:
                self.context.selection[2] = x
                self.context.selection[3] = y

    def on_mouse_release(self, x, y, button, modifiers):
        super().on_mouse_release(x, y, button, modifiers)
        if button == mouse.RIGHT:
            self.context.select()
            self.context.selection = None
        
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
