# from ui import Frame, Button, Entry, FloatEntry, Label, Subwindow
import ui
from core.rigidbody import RigidBody


class ToolBox(ui.Frame):
    def __init__(self, parent):
        super().__init__(1, 0, 80, parent.h, parent)
        self.build()

    def add_button(self, name, command):
        h = 40
        margin = 8
        top = margin + len(self.children)*(h + margin)

        bt = ui.Button(
            x=4, y=0,
            w=40, h=h,
            parent=self,
            text=name,
            command=command)
        bt.label.lab.color = (220, 220, 220, 255)
        bt.top = top
        bt.null_color = (0.12, 0.14, 0.15, 1)
        bt.color = (0.12, 0.14, 0.15, 1)
        bt.border_color = (0, 0, 0, 0)
        return bt
    
    def build(self):
        self.bt = self.add_button('Add', self.add_bt_function)
        self.bt = self.add_button('Force', self.force_bt_function)
        # self.add_force_menu = AddForceWindow(self.parent)
        # self.add_force_menu.is_visible = False
        # self.add_force_menu.x = 80
        # self.add_force_menu.top = 70

    def add_bt_function(self):
        self.parent.show_options()

    def force_bt_function(self):
        # self.add_force_menu.is_visible = True
        pass
    
    def draw(self, offset_x=0, offset_y=0):
        self.draw_children(self.x + offset_x, self.y + offset_y)
