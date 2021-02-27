from ui import widgets
from core import context_wrapper

ctx_wrapper = context_wrapper.ContextWrapper(0, 0)


class AddForceWindow(widgets.Subwindow):
    def __init__(self, parent):
        super().__init__(
            x=0, y=0,
            w=200, h=155, 
            caption='Adicionar força', 
            parent=parent)
        self.build()

    def build(self):
        label_x = widgets.Label(20, 0, 0, 0, parent=self.frame)
        label_x.top = 40
        label_x.lab.color = (120, 120, 120, 255)
        label_x.text = 'X:'
        self.entry_x = widgets.FloatEntry(40, 0, 140, 30, self.frame)
        self.entry_x.top = 20

        label_y = widgets.Label(20, 0, 0, 0, parent=self.frame)
        label_y.top = 80
        label_y.lab.color = (120, 120, 120, 255)
        label_y.text = 'Y:'
        self.entry_y = widgets.FloatEntry(40, 0, 140, 30, self.frame)
        self.entry_y.top = 60

        self.submit_bt = widgets.Button(
            x=20,
            y=20,
            w=160,
            h=30,
            parent=self.frame,
            command=self.submit,
            text='Aplicar'
        )
        self.submit_bt.label.lab.color = (50, 50, 50, 255)
        self.is_visible = False

        self.frame.add(label_x)
        self.frame.add(self.entry_x)
        self.frame.add(label_y)
        self.frame.add(self.entry_y)
        self.frame.add(self.submit_bt)
    
    def submit(self):
        x = self.entry_x.get_value()
        y = self.entry_y.get_value()

        for rb in ctx_wrapper.selected:
            rb.add_force(x, y)

        self.close()
