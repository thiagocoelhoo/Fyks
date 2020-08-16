from ui import Frame, Button


class Menu(Frame):
    def __init__(self, parent):
        super().__init__(0, 0, 0, 0, parent=parent)
        self.color = (0.05, 0.05, 0.05, 1)
        self.border_color = (0, 0, 0, 0.8)
        self.w = parent.w
        self.h = 30
        self.top = 0
    
    def add_button(self, text, command):
        bt = Button(
            x=len(self.content) * 70, y=0,
            w=70, h=28,
            text=text,
            command=command,
            parent=self
        )
        
        bt.null_color = (0, 0, 0, 0)
        bt.color = (0, 0, 0, 0)
        bt.border_color = (0, 0, 0, 0)
        bt.border_radius = 0