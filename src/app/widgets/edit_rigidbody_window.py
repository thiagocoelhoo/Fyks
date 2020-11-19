from ui import widgets


class EditRigidbodyWindow(widgets.Subwindow):
    def __init__(self, parent):
        super().__init__(
            x=0, y=0, 
            w=304, h=240,
            caption='Editar objeto', 
            parent=parent)
        self.target = None
        
        self.init_ui()

    def init_ui(self):
        super().init_ui()

        label_pos_x = widgets.Label(0, 0, 0, 16)
        label_pos_x.lab.color = (200, 200, 200, 255)
        label_pos_x.text = 'Posição X:'
        self.entry_pos_x = widgets.FloatEntry(0, 0, 130, 30)

        label_pos_y = widgets.Label(8, 0, 0, 16)
        label_pos_y.lab.color = (200, 200, 200, 255)
        label_pos_y.text = 'Posição Y:'
        self.entry_pos_y = widgets.FloatEntry(0, 0, 130, 30)

        label_vel_x = widgets.Label(0, 0, 0, 16)
        label_vel_x.lab.color = (200, 200, 200, 255)
        label_vel_x.text = 'Velocidade X:'
        self.entry_vel_x = widgets.FloatEntry(0, 0, 130, 30)
        
        label_vel_y = widgets.Label(0, 0, 0, 16)
        label_vel_y.lab.color = (200, 200, 200, 255)
        label_vel_y.text = 'Velocidade Y:'
        self.entry_vel_y = widgets.FloatEntry(0, 0, 130, 30)
        
        # self.edit_forces_bt = widgets.Button(12, 12, 110, 32, 
        #     text='Forças', command=self.close)
        # self.edit_forces_bt.label.lab.color = (50, 50, 50, 255)
        
        self.submit_bt = widgets.Button(12, 12, 110, 32, 
            text='Confirmar', command=self.close)
        self.submit_bt.label.lab.color = (50, 50, 50, 255)

        self.frame.add(label_pos_x)
        self.frame.add(self.entry_pos_x)
        self.frame.add(label_pos_y)
        self.frame.add(self.entry_pos_y)
        self.frame.add(label_vel_x)
        self.frame.add(self.entry_vel_x)
        self.frame.add(label_vel_y)
        self.frame.add(self.entry_vel_y)
        # self.frame.add(self.edit_forces_bt)
        self.frame.add(self.submit_bt)

        label_pos_x.top = 8
        label_pos_x.x = 12
        self.entry_pos_x.top = 32
        self.entry_pos_x.x = 12

        label_pos_y.top = 8
        label_pos_y.x = 162
        self.entry_pos_y.top = 32
        self.entry_pos_y.x = 162

        label_vel_x.top = 78
        label_vel_x.x = 12
        self.entry_vel_x.top = 102
        self.entry_vel_x.x = 12

        label_vel_y.top = 78
        label_vel_y.x = 162
        self.entry_vel_y.top = 102
        self.entry_vel_y.x = 162

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
