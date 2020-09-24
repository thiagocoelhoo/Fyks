from pyglet.window import mouse, key
from pyglet.gl import *

from ui import Frame, CustomMouseHandler
from core.render import Render, draw_circle
from graphicutils import graphicutils
from .context_wrapper import ContextWrapper
from .context_widgets import (
    AddRigidbodyWindow,
    RigidbodyInfoWindow,
    ToolBox,
)


class ContextFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_wrapper = ContextWrapper(self.w, self.h)
        self.mouse_handler = CustomMouseHandler()
        self.mouse_handler.on_double_click = self.on_double_click
        self.running = True

        self.build()

        self.KEYMAP = {
            (key.MOD_SHIFT, key.A): 'options',
            (16, key.HOME): 'home',
            (16, key.DELETE): 'delete',
            (16, key.SPACE): 'pause',
        }
    
    def build(self):
        self.toolbox = ToolBox(self)
        self.add_rb_win = AddRigidbodyWindow(self)
        self.rb_info_win = RigidbodyInfoWindow(self)
    
    def show_options(self):
        self.add_rb_win.x = self.mouse_handler.x
        self.add_rb_win.y = self.mouse_handler.y - self.add_rb_win.h
        self.add_rb_win.is_visible = True
    
    def on_resize(self, w, h):
        self.context_wrapper.resize(w, h)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.pressed:
            self.context_wrapper.on_mouse_scroll(x, y, scroll_x, scroll_y)
    
    def on_mouse_press(self, x, y, button, modifiers): 
        super().on_mouse_press(x, y, button, modifiers)
        if self.pressed:
            self.context_wrapper.on_mouse_press(x, y, button, modifiers)
            
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        if self.pressed:
            self.context_wrapper.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    
    def on_mouse_release(self, x, y, button, modifiers):
        super().on_mouse_release(x, y, button, modifiers)
        self.mouse_handler.on_mouse_release(x, y, button, modifiers)
        self.context_wrapper.on_mouse_release(x, y, button, modifiers)
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_handler.on_mouse_motion(x, y, dx, dy)
    
    def on_double_click(self, x, y, button, modifiers):
        self.context_wrapper.select_closer(x, y)
        if self.context_wrapper.selected:
            self.rb_info_win.x = x
            self.rb_info_win.y = y - self.rb_info_win.h
            self.rb_info_win.set_target(self.context_wrapper.selected[0])
            self.rb_info_win.is_visible = True

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        command = None

        for mod, sym in self.KEYMAP.keys():
            if modifiers & mod and symbol == sym:
                command = self.KEYMAP[(mod, sym)]
                break

        if command == 'options':
            self.show_options()
        elif command == 'home':
            self.context_wrapper.camera.to_home()
        elif command == 'delete':
            self.context_wrapper.delete_selected()
        elif command == 'pause':
            self.context_wrapper.toggle_pause()
    
    def draw(self, offset_x=0, offset_y=0):
        glColor4f(0.15, 0.15, 0.15, 1)
        graphicutils.draw_rect(
            self.x + offset_x,
            self.y + offset_y,
            self.w, self.h,
            GL_QUADS)
        self.context_wrapper.draw()
        self.draw_children(offset_x, offset_y)

    def update(self, dt):
        super().update(dt)
        self.context_wrapper.update(dt)