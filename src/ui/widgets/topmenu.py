from pyglet import gl

from ui import widgets


class Dropdown(widgets.Layout):
    def __init__(self, x, y, w, h, parent=None):
        super().__init__(x, y, w, h, parent=parent)
        self.max_width = 120
        self.button_height = 30
        self.border_radius = 3
        self.min_height = 0
        self.min_width = 0

    def add(self, element):
        super().add(element)
        self.max_height = self.height + 30
        self.height = self.max_height
        

    
class Menu(widgets.Layout):
    def __init__(self, parent=None):
        super().__init__(0, 0, 0, 0, 'vertical', parent)
        self.min_height = 30
        self.max_height = 30
        
        self.color = (0.12, 0.14, 0.15, 1)
        self.border_color = (0, 0, 0, 0.2)
    
    def add_button(self, name, command):
        bt = widgets.Button(
            x=0, y=0,
            w=70, h=28,
            text=name,
            command=command)
        bt.max_width = 70
        bt.max_height = 28
        bt.min_height = 28
        bt.label.lab.color = (255, 255, 255, 150)
        bt.null_color = (0, 0, 0, 0)
        bt.color = (0, 0, 0, 0)
        bt.border_color = (0, 0, 0, 0)
        bt.border_radius = 0
        self.add(bt)
    
    def add_dropdown(self, name, options):
        pos_x = len(self.elements) * 70
        dropdown = Dropdown(4, 0, 120, 0)
        dropdown.is_visible = False
        dropdown.margin_top = 34

        for i, (op_name, command) in enumerate(options):
            bt = widgets.Button(
                x=0, y=0,
                w=140, h=28,
                text=op_name,
                command=command)
            bt.null_color = (0, 0, 0, 0)
            bt.pressed_color = (0.1, 0.8, 1, 0.4)
            bt.color = (0, 0, 0, 0)
            bt.border_color = (0, 0, 0, 0)
            dropdown.add(bt)
        
        self.add_button(name, command=dropdown.toggle_is_visible)
        return dropdown
