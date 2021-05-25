from pyglet.window import mouse, key
from pyglet import gl

import app
import graphicutils as gu
from ui import widgets, handlers
from core.context_wrapper import ContextWrapper
from constants import *


class ContextFrame(widgets.Frame):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.ctx_wrapper = ContextWrapper(self.width, self.height)
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
        
        self.add_object_window.x = 4
        self.add_object_window.y = 4

        self.add_force_window.x = 4
        self.add_force_window.y = 4

        self.add(self.timeline)
        self.add(self.add_object_window)
        self.add(self.add_force_window)
        self.add(self.edit_object_window)
        self.add(self.edit_forces_window)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.pressed:
            if scroll_y > 0:
                self.ctx_wrapper.zoom_in()
            elif scroll_y < 0:
                self.ctx_wrapper.zoom_out()
    
    def on_mouse_press(self, x, y, button, modifiers): 
        super().on_mouse_press(x, y, button, modifiers)
        x -= self.x
        y -= self.y

        if self.pressed:
            mode = self.ctx_wrapper.get_mode()
            cam = self.ctx_wrapper.get_camera()
            x_, y_ = cam.get_relative_position(x, y)

            if button == mouse.LEFT:    
                if mode == SELECT_MODE:
                    self.ctx_wrapper.set_selection_area(x, y, x, y)
                elif mode == RULER_MODE:
                    self.ctx_wrapper.set_ruler(x_, y_, x_, y_)
                elif mode == MOVE_MODE:
                    pass
            
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        x -= self.x
        y -= self.y

        if self.pressed:
            if buttons == mouse.LEFT:
                mode = self.ctx_wrapper.get_mode()
                cam = self.ctx_wrapper.get_camera()
                x_, y_ = cam.get_relative_position(x, y)

                if mode == SELECT_MODE:
                    x1, y1, x2, y2 = self.ctx_wrapper.get_selection_area()
                    self.ctx_wrapper.set_selection_area(x1, y1, x, y)
                elif mode == RULER_MODE:
                    x1, y1, x2, y2 = self.ctx_wrapper.get_ruler()
                    self.ctx_wrapper.set_ruler(x1, y1, x_, y_)
                elif mode == MOVE_MODE:
                    self.ctx_wrapper.move_selected(dx, dy)
            elif buttons == mouse.RIGHT:
                self.ctx_wrapper.move_camera(-dx,-dy)
    
    def on_mouse_release(self, x, y, button, modifiers):
        super().on_mouse_release(x, y, button, modifiers)
        self.mouse_handler.on_mouse_release(x, y, button, modifiers)

        if self.pressed:
            if button == mouse.LEFT:
                mode = self.ctx_wrapper.get_mode()
                if mode == SELECT_MODE:
                    self.ctx_wrapper.select_area()
                    self.ctx_wrapper.set_selection_area(0, 0, 0, 0)
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_handler.on_mouse_motion(x, y, dx, dy)
    
    def on_double_click(self, x, y, button, modifiers):
        self.ctx_wrapper.select_closer(
            x=x - self.global_position[0], 
            y=y - self.global_position[1])
        
        selected = self.ctx_wrapper.get_selected()
        if selected:
            self.edit_object_window.show()
            self.edit_object_window.x = x
            self.edit_object_window.top = y
            self.edit_object_window.set_target(selected[0])
    
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
            self.ctx_wrapper.set_move_mode()
        elif command == 'home':
            self.ctx_wrapper.camera_to_home()
        elif command == 'delete':
            self.ctx_wrapper.delete_selected()
        elif command == 'pause':
            self.ctx_wrapper.toggle_pause()
    
    def resize(self, width, height):
        super().resize(width, height)
        self.ctx_wrapper.resize(int(width), int(height))
        self.timeline.resize(width - 20, 20)
    
    def draw(self):
        self.update_viewport()
        gl.glColor3f(*app.colors.CONTEXT_BACKGROUND_COLOR)
        gu.draw_rect(0, 0, self.width, self.height, gl.GL_QUADS)
        
        self.ctx_wrapper.draw_ctx()
        self.draw_widgets()

    def update(self, dt):
        super().update(dt)
        self.ctx_wrapper.update(dt)
