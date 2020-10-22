import pyglet

import ui
from core.rigidbody import RigidBody
from app import colors

from .add_force_window import AddForceWindow
from .add_rigidbody_window import AddRigidbodyWindow

add_object_icon = pyglet.image.load('assets/add_object_icon.png')
add_force_icon = pyglet.image.load('assets/add_force_icon.png')
ruler_icon = pyglet.image.load('assets/ruler_icon.png')


class ToolBox(ui.Frame):
    def __init__(self, parent):
        super().__init__(0, 0, 60, parent.h, parent)
        self.color = colors.TOOLBOX_COLOR
        self.border_color = (0, 0, 0, 0.2)
        self.build()
    
    def add_icon_button(self, icon, command):
        h = 48
        margin = 6
        top = margin + len(self.children)*(h + margin)
        bt = ui.Iconbutton(
            x=6, y=0,
            w=48, h=h,
            parent=self,
            image=icon,
            command=command
        )
        bt.top = top
    
    def build(self):
        self.add_bt = self.add_icon_button(add_object_icon, self.add_bt_function)
        self.force_bt = self.add_icon_button(add_force_icon, self.force_bt_function)
        self.ruler_bt = self.add_icon_button(ruler_icon, self.force_bt_function)
        self.add_force_window = AddForceWindow(self.parent)
        self.add_force_window.is_visible = False
        self.add_force_window.x = 80
        self.add_force_window.top = 70

    def add_bt_function(self):
        self.parent.show_options()

    def force_bt_function(self):
        self.add_force_window.is_visible = True
    
    def set_ruler_mode(self):
        self.parent.context_wrapper.mode = 2
    
    def draw(self, offset_x=0, offset_y=0):
        super().draw(offset_x, offset_y)
        self.draw_children(self.x + offset_x, self.y + offset_y)
