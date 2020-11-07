from ui import widgets
from context import context_wrapper

wrapper = context_wrapper.ContextWrapper(0, 0)


class EditForcesWindow(widgets.Subwindow):
    def __init__(self, parent):
        super().__init__(
            x=0, y=0, 
            w=286, h=150, 
            caption='Editar forças', 
            parent=parent
        )
        self.init_ui()

    def init_ui(self):
        super().init_ui()
        self.list_viewer = widgets.List(12, 54, 262, 84, self.frame)
        self.close_bt = widgets.Button(
            x=12, y=12,
            w=100, h=30,
            parent=self.frame,
            command=self.close,
            text='Fechar'
        )
        self.add_bt = widgets.Button(
            x=124, y=12,
            w=150, h=30,
            parent=self.frame,
            text='Adicionar força'
        )
        self.close_bt.label.lab.color = (50, 50, 50, 255)
        self.add_bt.label.lab.color = (50, 50, 50, 255)
        self.is_visible = False
