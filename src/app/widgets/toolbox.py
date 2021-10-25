from ui import widgets
from app import colors
from constants import *


class ToolBox(widgets.Layout):
    def __init__(self):
        super().__init__(0, 0, 0, 0)
        self.max_width = 60
        self.color = colors.TOOLBOX_COLOR
        self.border_color = (0, 0, 0, 0.2)
        self.button_size = 48

    def add_tool_bt(self, icon, command):
        bt = widgets.Iconbutton(6, 0, 0, 0, image=icon, command=command)
        bt.min_height = self.button_size
        bt.max_height = self.button_size
        bt.margin_top = 6
        self.add(bt)
    
    def set_tools(self, tools):
        self.elements.clear()
        for icon, command in tools:    
            self.add_tool_bt(icon, command)
