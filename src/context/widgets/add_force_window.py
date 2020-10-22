import ui
from context import context_wrapper

wrapper = context_wrapper.ContextWrapper(0, 0)


class AddForceWindow(ui.Subwindow):
    def __init__(self, parent):
        super().__init__(0, 0, 200, 155, caption='Adicionar força', parent=parent)
        self.build()

    def build(self):
        label_x = ui.Label(20, 0, 0, 0, parent=self.frame)
        label_x.top = 40
        label_x.lab.color = (120, 120, 120, 255)
        label_x.text = 'X:'
        self.entry_x = ui.FloatEntry(40, 0, 140, 30, self.frame)
        self.entry_x.top = 20

        label_y = ui.Label(20, 0, 0, 0, parent=self.frame)
        label_y.top = 80
        label_y.lab.color = (120, 120, 120, 255)
        label_y.text = 'Y:'
        self.entry_y = ui.FloatEntry(40, 0, 140, 30, self.frame)
        self.entry_y.top = 60

        self.submit_bt = ui.Button(
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

    def submit(self):
        x = self.entry_x.get_value()
        y = self.entry_y.get_value()

        for rb in wrapper.selected:
            rb.add_force(x, y)

        self.is_visible = False
