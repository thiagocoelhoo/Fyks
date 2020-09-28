import ui
from core.rigidbody import RigidBody
from app import colors

from .add_force_window import AddForceWindow
from .add_rigidbody_window import AddRigidbodyWindow


class ToolBox(ui.Frame):
    def __init__(self, parent):
        super().__init__(0, 0, 60, parent.h, parent)
        self.color = colors.TOOLBOX_COLOR
        self.border_color = (0, 0, 0, 0.2)
        self.build()

    def add_button(self, name, command):
        h = 30
        margin = 4
        top = margin + len(self.children)*(h + margin)

        bt = ui.Button(
            x=4, y=0,
            w=42, h=h,
            parent=self,
            text=name,
            command=command)
        bt.label.lab.color = (220, 220, 220, 255)
        bt.top = top
        bt.null_color = colors.TOOLBOX_BUTTON_COLOR
        bt.color = colors.TOOLBOX_BUTTON_COLOR
        bt.border_color = (0, 0, 0, 0)
        bt.border_radius = 3
        return bt
    
    def build(self):
        self.bt = self.add_button('Add', self.add_bt_function)
        self.bt = self.add_button('Force', self.force_bt_function)
        self.add_force_window = AddForceWindow(self.parent)
        self.add_force_window.is_visible = False
        self.add_force_window.x = 80
        self.add_force_window.top = 70

    def add_bt_function(self):
        self.parent.show_options()

    def force_bt_function(self):
        self.add_force_window.is_visible = True
    
    def draw(self, offset_x=0, offset_y=0):
        super().draw(offset_x, offset_y)
        self.draw_children(self.x + offset_x, self.y + offset_y)
