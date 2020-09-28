from ui import Frame, Button, Entry, FloatEntry, Label, Subwindow


class EditRigidbodyWindow(Subwindow):
    def __init__(self, parent):
        super().__init__(0, 0, 300, 250,
        title='Rb info', parent=parent)
        self.target = None
        self.build()
    
    def set_target(self, obj):
        self.target = obj

    def build(self):
        label_pos_x = Label(20, 0, 0, 0, parent=self.frame)
        label_pos_x.top = 40
        label_pos_x.lab.color = (120, 120, 120, 255)
        label_pos_x.text = 'posição x'
        self.entry_pos_x = FloatEntry(120, 0, 160, 30, self.frame)
        self.entry_pos_x.top = 20

        label_pos_y = Label(20, 0, 0, 0, parent=self.frame)
        label_pos_y.top = 80
        label_pos_y.lab.color = (120, 120, 120, 255)
        label_pos_y.text = 'posição y'
        self.entry_pos_y = FloatEntry(120, 0, 160, 30, self.frame)
        self.entry_pos_y.top = 60

        label_vel_x = Label(20, 0, 0, 0, parent=self.frame)
        label_vel_x.top = 120
        label_vel_x.lab.color = (120, 120, 120, 255)
        label_vel_x.text = 'velocidade x'
        self.entry_vel_x = FloatEntry(120, 0, 160, 30, self.frame)
        self.entry_vel_x.top = 100

        label_vel_y = Label(20, 0, 0, 0, parent=self.frame)
        label_vel_y.top = 160
        label_vel_y.lab.color = (120, 120, 120, 255)
        label_vel_y.text = 'velocidade y'
        self.entry_vel_y = FloatEntry(120, 0, 160, 30, self.frame)
        self.entry_vel_y.top = 140

        self.submit_bt = Button(
            x=20,
            y=20,
            w=260,
            h=30,
            text='Ok',
            command=self.close,
            parent=self.frame)
        self.submit_bt.label.lab.color = (50, 50, 50, 255)
        self.is_visible = False
    
    def update(self, dt):
        if self.target is not None:
            pos_x_str = str(self.target.x)
            pos_y_str = str(self.target.y)
            vel_x_str = str(self.target.velocity[0])
            vel_y_str = str(self.target.velocity[1])

            if not self.entry_pos_x.pressed:
                self.entry_pos_x.text = pos_x_str[:10]
            else:
                self.target.x = self.entry_pos_x.get_value()

            if not self.entry_pos_y.pressed:
                self.entry_pos_y.text = pos_y_str[:10]
            else:
                self.target.y = self.entry_pos_x.get_value()

            if not self.entry_vel_x.pressed:
                self.entry_vel_x.text = vel_x_str[:10]
            else:
                self.target.velocity[0] = self.entry_vel_x.get_value()

            if not self.entry_vel_y.pressed:
                self.entry_vel_y.text = vel_y_str[:10]
            else:
                self.target.velocity[1] = self.entry_vel_y.get_value()
