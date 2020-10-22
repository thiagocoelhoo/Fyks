from pyglet.window import mouse, key
from pyglet import gl

from ui import Frame, CustomMouseHandler
from .context_wrapper import ContextWrapper
from context import widgets
from app import colors
import graphicutils as gu


class ContextFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_wrapper = ContextWrapper(self.w, self.h)
        self.mouse_handler = CustomMouseHandler()
        self.mouse_handler.on_double_click = self.on_double_click
        self.running = True

        self.KEYMAP = {
            (key.MOD_SHIFT, key.A): 'options',
            (None, key.HOME): 'home',
            (None, key.DELETE): 'delete',
            (None, key.SPACE): 'pause',
        }

        self.init_ui()
    
    def init_ui(self):
        self.toolbox = widgets.ToolBox(self)
        self.add_rb_win = widgets.AddRigidbodyWindow(self)
        self.edit_rb_win = widgets.EditRigidbodyWindow(self)
        self.edit_forces_window = widgets.EditForcesWindow(self)
        self.timeline = widgets.Timeline(x=70, y=10, parent=self)

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
        self.context_wrapper.select_closer(x - 60, y)
        if self.context_wrapper.selected:
            self.edit_rb_win.show()
            self.edit_rb_win.x = x
            self.edit_rb_win.y = y - self.edit_rb_win.h
            self.edit_rb_win.set_target(self.context_wrapper.selected[0])

    def on_key_press(self, symbol, modifiers):
        super().on_key_press(symbol, modifiers)
        command = None
        for mod, sym in self.KEYMAP.keys():
            if symbol == sym:
                if mod is None or modifiers & mod:
                    command = self.KEYMAP[(mod, sym)]
                    break

        if command == 'options':
            self.show_options()
        elif command == 'home':
            self.context_wrapper.camera_to_home()
        elif command == 'delete':
            self.context_wrapper.delete_selected()
        elif command == 'pause':
            self.context_wrapper.toggle_pause()
        self.context_wrapper.on_key_press(symbol, modifiers)
    
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