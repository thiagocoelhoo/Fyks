import pyglet

import ui
from core.rigidbody import RigidBody
from app import colors
from constants import *

add_object_icon = pyglet.image.load('assets/add_object_icon.png')
add_force_icon = pyglet.image.load('assets/add_force_icon.png')
ruler_icon = pyglet.image.load('assets/ruler_icon.png')


class ToolBox(ui.Frame):
    def __init__(self, parent):
        super().__init__(0, 0, 60, parent.h, parent)
        self.color = colors.TOOLBOX_COLOR
        self.border_color = (0, 0, 0, 0.2)
        self.button_size = 48
        self.button_margin = 6
        self.init_ui()
    
    def init_ui(self):
        tool_list = [
            (add_object_icon, self.add_bt_function),
            (add_force_icon, self.force_bt_function),
            (ruler_icon, self.ruler_bt_function),
        ]
        tool_buttons = list(self.set_tools(tool_list))
        self.add_bt = tool_buttons[0]
        self.force_bt = tool_buttons[1]
        self.ruler_bt = tool_buttons[2]
    
    def set_tools(self, tools):
        self.children.clear()
        cursor = self.button_margin

        for icon, command in tools:    
            bt = ui.Iconbutton(
                x=self.button_margin, y=0,
                w=self.button_size, h=self.button_size,
                parent=self,
                image=icon,
                command=command)
            bt.top = cursor
            cursor += self.button_margin + self.button_size
            yield bt
    
    def add_bt_function(self):
        self.parent.add_object_window.show()

    def force_bt_function(self):
        self.parent.add_force_window.show()
    
    def ruler_bt_function(self):
        # self.parent.context_wrapper.mode = RULER_MODE
        pass
    
    def draw(self, offset_x=0, offset_y=0):
        super().draw(offset_x, offset_y)
        self.draw_children(self.x + offset_x, self.y + offset_y)
