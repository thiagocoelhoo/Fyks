from ui import widgets


class EditRigidbodyWindow(widgets.Subwindow):
    def __init__(self, parent):
        super().__init__(
            x=0, y=0, 
            w=380, h=250,
            caption='Editar objeto', 
            parent=parent
        )
        self.target = None
        self.init_ui()

    def init_ui(self):
        super().init_ui()
        
        label_pos_x = widgets.Label(12, 0, 0, 0, parent=self.frame)
        label_pos_x.top = 20
        label_pos_x.lab.color = (200, 200, 200, 255)
        label_pos_x.text = 'Posição X:'
        self.entry_pos_x = widgets.FloatEntry(12, 0, 160, 30, self.frame)
        self.entry_pos_x.top = 28

        label_pos_y = widgets.Label(190, 0, 0, 0, parent=self.frame)
        label_pos_y.top = 20
        label_pos_y.lab.color = (200, 200, 200, 255)
        label_pos_y.text = 'Posição Y:'
        self.entry_pos_y = widgets.FloatEntry(190, 0, 160, 30, self.frame)
        self.entry_pos_y.top = 28

        label_vel_x = Label(12, 0, 0, 0, parent=self.frame)
        label_vel_x.top = 74
        label_vel_x.lab.color = (200, 200, 200, 255)
        label_vel_x.text = 'Velocidade X:'
        self.entry_vel_x = widgets.FloatEntry(12, 0, 160, 30, self.frame)
        self.entry_vel_x.top = 82

        label_vel_y = Label(190, 0, 0, 0, parent=self.frame)
        label_vel_y.top = 74
        label_vel_y.lab.color = (200, 200, 200, 255)
        label_vel_y.text = 'Velocidade Y:'
        self.entry_vel_y = widgets.FloatEntry(190, 0, 160, 30, self.frame)
        self.entry_vel_y.top = 82

        self.submit_bt = widgets.Button(
            x=12,
            y=12,
            w=150,
            h=30,
            text='Confirmar',
            command=self.close,
            parent=self.frame)
        self.submit_bt.label.lab.color = (50, 50, 50, 255)
        self.is_visible = False
    
    def set_target(self, obj):
        self.target = obj

    def update(self, dt):
        if self.target is not None:
            pos_x_str = str(self.target.position[0])
            pos_y_str = str(self.target.position[1])
            vel_x_str = str(self.target.velocity[0])
            vel_y_str = str(self.target.velocity[1])

            if not self.entry_pos_x.pressed:
                self.entry_pos_x.text = pos_x_str[:10]
            else:
                self.target.position[0] = self.entry_pos_x.get_value()

            if not self.entry_pos_y.pressed:
                self.entry_pos_y.text = pos_y_str[:10]
            else:
                self.target.position[1] = self.entry_pos_y.get_value()

            if not self.entry_vel_x.pressed:
                self.entry_vel_x.text = vel_x_str[:10]
            else:
                self.target.velocity[0] = self.entry_vel_x.get_value()

            if not self.entry_vel_y.pressed:
                self.entry_vel_y.text = vel_y_str[:10]
            else:
                self.target.velocity[1] = self.entry_vel_y.get_value()
        