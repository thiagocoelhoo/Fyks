from ui import widgets


class AddRigidbodyWindow(widgets.Subwindow):
    def __init__(self, parent):
        super().__init__(
            x=0, y=0,
            w=200, h=155,
            caption='Adicionar objeto', 
            parent=parent
        )
        self.init_ui()

    def init_ui(self):
        super().init_ui()
        
        label_x = Label(20, 0, 0, 0, parent=self.frame)
        label_x.top = 40
        label_x.lab.color = (120, 120, 120, 255)
        label_x.text = 'X:'
        self.entry_x = FloatEntry(40, 0, 140, 30, self.frame)
        self.entry_x.top = 20

        label_y = Label(20, 0, 0, 0, parent=self.frame)
        label_y.top = 80
        label_y.lab.color = (120, 120, 120, 255)
        label_y.text = 'Y:'
        self.entry_y = FloatEntry(40, 0, 140, 30, self.frame)
        self.entry_y.top = 60

        self.submit_bt = Button(
            x=20,
            y=20,
            w=160,
            h=30,
            parent=self.frame,
            command=self.submit,
            text='Adicionar'
        )

        self.submit_bt.label.lab.color = (50, 50, 50, 255)
        self.is_visible = False

    def submit(self):
        x = self.entry_x.get_value()
        y = self.entry_y.get_value()
        self.parent.context_wrapper.add_object(
            position=(x, y),
            velocity=(0, 0),
            acceleration=(0, 0),
            mass=1,
            charge=0
        )
        self.is_visible = False

