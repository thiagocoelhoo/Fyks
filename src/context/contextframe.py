import pickle

from pyglet.window import mouse, key
from pyglet.gl import *

from ui import Frame, CustomMouseHandler
from core.render import Render, draw_circle
from graphicutils import graphicutils
from .context import Context
from .context_widgets import (
    AddRigidbodyWindow,
    RigidbodyInfoWindow,
    ToolBox,
)


class ContextFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = Context(0, 0, self.w, self.h)
        self.context_render = Render(self.context.camera)
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
    
    def on_resize(self, w, h):
        self.context.camera.w = w
        self.context.camera.h = h
    
    def show_options(self):
        self.add_rb_win.x = self.mouse_handler.x
        self.add_rb_win.y = self.mouse_handler.y - self.add_rb_win.h
        self.add_rb_win.is_visible = True

    def pause(self):
        self.running = not self.running
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.pressed:
            if scroll_y < 0:
                if self.context.camera.zoom > 0.05:
                    self.context.camera.zoom -= 0.05
            elif scroll_y > 0:
                self.context.camera.zoom += 0.05
    
    def on_mouse_press(self, x, y, button, modifiers): 
        super().on_mouse_press(x, y, button, modifiers)
        
        if self.pressed and button == mouse.RIGHT:
            self.context.selection = [x, y, x, y]

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        if self.pressed:
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
            self.rb_info_win.x = x
            self.rb_info_win.y = y - self.rb_info_win.h
            self.rb_info_win.set_target(self.context.selected[0])
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
            self.context.camera.to_home()
        elif command == 'delete':
            self.context.delete_selected()
        elif command == 'pause':
            self.pause()
            
                
    def draw_overlayer(self):
        zoom = self.context.camera.zoom
        for obj in self.context.selected:
            if self.context.camera.collide(obj):
                objx = int(obj.x * zoom + self.context.camera.centerx)
                objy = int(obj.y * zoom + self.context.camera.centery)
                draw_circle(
                    objx,
                    objy, 
                    25 * zoom,
                    (1, 0.2, 0.2, 1),
                )
        
        if self.context.selection is not None:
            x1, y1, x2, y2 = self.context.selection
            glColor4f(0.1, 0.1, 0.3, 0.2)
            rect = (x1, y1, x2, y1, x2, y2, x1, y2)
            pyglet.graphics.draw(
                4, GL_QUADS,
                ('v2f', rect)
            )
            glColor4f(0.3, 0.3, 0.8, 0.5)
            pyglet.graphics.draw(
                4, GL_LINE_LOOP,
                ('v2f', rect)
            )

    def draw(self, offset_x=0, offset_y=0):
        glColor4f(0.15, 0.15, 0.15, 1)
        graphicutils.draw_rect(
            self.x + offset_x,
            self.y + offset_y,
            self.w, self.h,
            GL_QUADS)
        
        self.context_render.draw_grid()
        self.context_render.draw_axes()
        for obj in self.context.objects:
            self.context_render.render(obj)
        
        self.draw_overlayer()
        self.draw_children(offset_x, offset_y)

    def update(self, dt):
        super().update(dt)
        if self.running:
            self.context.update(dt)
