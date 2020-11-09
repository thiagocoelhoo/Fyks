from pyglet.window import mouse, key
from pyglet import gl

import app
import graphicutils as gu
from ui import widgets, elements, handlers
from core.context_wrapper import ContextWrapper
from constants import *


class ContextFrame(widgets.Frame):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        
        self.context_wrapper = ContextWrapper(self.width, self.height)
        self.mouse_handler = handlers.CustomMouseHandler()
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
        self.timeline = app.widgets.Timeline(x=10, y=10)
        self.add_object_window = app.widgets.AddRigidbodyWindow(self)
        self.add_force_window = app.widgets.AddForceWindow(self)
        self.edit_object_window = app.widgets.EditRigidbodyWindow(self)
        self.edit_forces_window = app.widgets.EditForcesWindow(self)
        self.add_force_window.show()
        
        self.add(self.timeline)

    def set_ruler_mode(self):
        self.context_wrapper.mode = RULER_MODE

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
        pass
    
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
    
    def resize(self, width, height):
        super().resize(width, height)
        self.context_wrapper.resize(int(width), int(height))
        self.timeline.resize(width - 20, 24)

    def draw(self, offset_x=0, offset_y=0):
        x = self.x + offset_x
        y = self.y + offset_y
        
        gl.glColor3f(*app.colors.CONTEXT_BACKGROUND_COLOR)
        gu.draw_rect(x, y, self.width, self.height, gl.GL_QUADS)
        self.context_wrapper.draw(x, y)
        self.draw_widgets(x, y)

    def update(self, dt):
        super().update(dt)
        self.context_wrapper.update(dt)
