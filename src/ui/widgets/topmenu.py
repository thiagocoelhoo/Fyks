from ui import widgets


class Menu(widgets.Layout):
    def __init__(self, parent=None):
        super().__init__(0, 0, 200, 200, 'vertical', parent)
        self.min_height = 30
        self.max_height = 30
        
        self.color = (0.12, 0.14, 0.15, 1)
        self.border_color = (0, 0, 0, 0.2)
    
    def add_button(self, name, command):
        bt = widgets.Button(
            x=len(self.elements) * 70, y=0,
            w=70, h=28,
            text=name,
            command=command
        )
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
        dropdown_height = len(options) * 30

        dropdown = widgets.Layout(pos_x, 0, 140, dropdown_height, self.parent)
        dropdown.top = 30
        dropdown.is_visible = False
        
        for i, (op_name, command) in enumerate(options):
            bt = widgets.Button(
                x=0, y=0,
                w=140, h=28,
                text=op_name,
                command=command)
            bt.top = 30*i
            bt.null_color = (0, 0, 0, 0)
            bt.color = (0, 0, 0, 0)
            bt.border_color = (0, 0, 0, 0)
            bt.border_radius = 0
            dropdown.add(bt)
        
        self.add_button(name, command=dropdown.toggle_is_visible)
    