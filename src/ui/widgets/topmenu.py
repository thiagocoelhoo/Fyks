from ui import Frame, Button


class Menu(Frame):
    def __init__(self, parent):
        super().__init__(0, 0, 0, 0, parent=parent)
        self.color = (0.12, 0.14, 0.15, 1)
        self.border_color = (0, 0, 0, 0.2)
        self.w = parent.w
        self.h = 30
        self.top = 0
    
    def add_button(self, name, command):
        bt = Button(
            x=len(self.children) * 70, y=0,
            w=70, h=28,
            text=name,
            command=command,
            parent=self
        )
        bt.label.lab.color = (255, 255, 255, 150)
        bt.null_color = (0, 0, 0, 0)
        bt.color = (0, 0, 0, 0)
        bt.border_color = (0, 0, 0, 0)
        bt.border_radius = 0
    
    def add_dropdown(self, name, options):
        pos_x = len(self.children) * 70

        dropdown_height = len(options) * 30
        dropdown = Frame(
            x=pos_x, y=0,
            w=140, h=dropdown_height,
            parent=self.parent
        )
        dropdown.top = 30
        dropdown.is_visible = False
        
        for i, (op_name, command) in enumerate(options):
            bt = Button(
                x=0, y=0,
                w=140, h=28,
                text=op_name,
                command=command,
                parent=dropdown)
            bt.top = 30*i
            bt.null_color = (0, 0, 0, 0)
            bt.color = (0, 0, 0, 0)
            bt.border_color = (0, 0, 0, 0)
            bt.border_radius = 0
            
        main_bt = Button(
            x=pos_x, y=0,
            w=70, h=28,
            text=name,
            command=dropdown.toggle_is_visible,
            parent=self)
        main_bt.label.lab.color = (255, 255, 255, 150)
        main_bt.null_color = (0, 0, 0, 0)
        main_bt.color = (0, 0, 0, 0)
        main_bt.border_color = (0, 0, 0, 0)
        main_bt.border_radius = 0