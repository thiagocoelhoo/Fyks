from pyglet.window import mouse, key
from pyglet import gl

import graphicutils as gu
from app import colors
from ui import Frame, CustomMouseHandler
from .context_wrapper import ContextWrapper
from context import widgets
from constants import *


class ContextFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_wrapper = ContextWrapper(self.w, self.h)
        self.mouse_handler = CustomMouseHandler()
        self.mouse_handler.on_double_click = self.on_double_click

        self.KEYMAP = {
            (key.MOD_SHIFT, key.A): 'add object',
            (key.MOD_SHIFT, key.F): 'add force',
            (key.MOD_SHIFT, key.M): 'move object',
            (None, key.HOME): 'home',
            (None, key.DELETE): 'delete',
            (None, key.SPACE): 'pause'}

        self.init_ui()
    
    def init_ui(self):
        self.timeline = widgets.Timeline(x=70, y=10, parent=self)
        self.toolbox = widgets.ToolBox(self)

        self.add_object_window = widgets.AddRigidbodyWindow(self)
        self.add_force_window = widgets.AddForceWindow(self)
        self.edit_object_window = widgets.EditRigidbodyWindow(self)
        self.edit_forces_window = widgets.EditForcesWindow(self)

    def set_ruler_mode(self):
        self.context_wrapper.mode = RULER_MODE
    
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
        self.context_wrapper.select_closer(x - 60, y)
        if self.context_wrapper.selected:
            self.edit_object_window.show()
            self.edit_object_window.x = x
            self.edit_object_window.top = y
            self.edit_object_window.set_target(self.context_wrapper.selected[0])

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        command = None
        for mod, sym in self.KEYMAP.keys():
            if symbol == sym:
                if mod is None or modifiers & mod:
                    command = self.KEYMAP[(mod, sym)]
                    break

        if command == 'add object':
            self.add_object_window.show()
        elif command == 'add force':
            self.add_force_window.show()
        elif command == 'move object':
            self.context_wrapper.mode = MOVE_MODE
        elif command == 'home':
            self.context_wrapper.camera_to_home()
        elif command == 'delete':
            self.context_wrapper.delete_selected()
        elif command == 'pause':
            self.context_wrapper.toggle_pause()
    
    def draw(self, offset_x=0, offset_y=0):
        gl.glColor3f(*colors.CONTEXT_BACKGROUND_COLOR)
        gu.draw_rect(
            self.x + offset_x,
            self.y + offset_y,
            self.w, self.h,
            gl.GL_QUADS)
        self.context_wrapper.draw(60, 0)
        self.draw_children(offset_x, offset_y)

    def update(self, dt):
        super().update(dt)
        self.context_wrapper.update(dt)