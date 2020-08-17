import warnings
import string

import pyglet

from ui import Frame, Button, Entry, FloatEntry, Label, Subwindow
from graphicutils import graphicutils
from core.rigidbody import RigidBody


class ContextOptionsMenu(Subwindow):
    def __init__(self, parent):
        super().__init__(0, 0, 200, 155,
            title='Add rb', parent=parent)
        self.build()

    def build(self):
        label_x = Label(20, 0, 0, 0, parent=self.frame)
        label_x.top = 40
        label_x.lab.color = (120, 120, 120, 255)
        label_x.text = 'x'
        self.entry_x = FloatEntry(40, 0, 140, 30, self.frame)
        self.entry_x.top = 20

        label_y = Label(20, 0, 0, 0, parent=self.frame)
        label_y.top = 80
        label_y.lab.color = (120, 120, 120, 255)
        label_y.text = 'y'
        self.entry_y = FloatEntry(40, 0, 140, 30, self.frame)
        self.entry_y.top = 60

        self.submit_bt = Button(
            x=20,
            y=20,
            w=160,
            h=30,
            parent=self.frame,
            command=self.submit,
            text='Submit'
        )

        self.display = False

    def submit(self):
        x = self.entry_x.get_value()
        y = self.entry_y.get_value()
        rb = RigidBody(
            position=(x, y),
            velocity=(0, 0),
            acceleration=(0, 0),
            mass=1,
            charge=0
        )
        self.parent.context.objects.append(rb)

        self.display = False


class AddForceMenu(Subwindow):
    def __init__(self, parent):
        super().__init__(0, 0, 200, 155, 
            title='Add force', parent=parent)
        self.build()

    def build(self):
        label_x = Label(20, 0, 0, 0, parent=self.frame)
        label_x.top = 40
        label_x.lab.color = (120, 120, 120, 255)
        label_x.text = 'x'
        self.entry_x = FloatEntry(40, 0, 140, 30, self.frame)
        self.entry_x.top = 20

        label_y = Label(20, 0, 0, 0, parent=self.frame)
        label_y.top = 80
        label_y.lab.color = (120, 120, 120, 255)
        label_y.text = 'y'
        self.entry_y = FloatEntry(40, 0, 140, 30, self.frame)
        self.entry_y.top = 60

        self.submit_bt = Button(
            x=20,
            y=20,
            w=160,
            h=30,
            parent=self.frame,
            command=self.submit,
            text='Apply'
        )

        self.display = False

    def submit(self):
        x = self.entry_x.get_value()
        y = self.entry_y.get_value()

        for rb in self.parent.context.selected:
            rb.add_force(x, y)

        self.display = False


class RigidbodyInfoWindow(Subwindow):
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

        self.display = False
    
    def update(self, dt):
        if self.target is not None:
            pos_x_str = str(self.target.x)
            pos_y_str = str(self.target.y)
            vel_x_str = str(self.target.velocity[0])
            vel_y_str = str(self.target.velocity[1])

            if not self.entry_pos_x.activated:
                self.entry_pos_x.text = pos_x_str[:10]
            else:
                self.target.x = self.entry_pos_x.get_value()

            if not self.entry_pos_y.activated:
                self.entry_pos_y.text = pos_y_str[:10]
            else:
                self.target.y = self.entry_pos_x.get_value()

            if not self.entry_vel_x.activated:
                self.entry_vel_x.text = vel_x_str[:10]
            else:
                self.target.velocity[0] = self.entry_vel_x.get_value()

            if not self.entry_vel_y.activated:
                self.entry_vel_y.text = vel_y_str[:10]
            else:
                self.target.velocity[1] = self.entry_vel_y.get_value()


class ToolBox(Frame):
    def __init__(self, parent):
        super().__init__(1, 0, 80, parent.context.h, parent)
        self.build()

    def add_button(self, name, command):
        h = 30
        margin = 8
        top = margin + len(self.content)*(h + margin)
        
        bt = Button(
            x=4, y=0,
            w=60, h=h,
            parent=self,
            text=name,
            command=command)
        bt.top = top
        bt.null_color = (0.05, 0.05, 0.15, 0.4)
        bt.color = (0.05, 0.05, 0.15, 0.4)
        bt.border_color = (0.3, 0.3, 0.8, 0.5)

        return bt
    
    def build(self):
        self.bt = self.add_button('Add', self.add_bt_function)
        self.bt = self.add_button('Force', self.force_bt_function)
        
        self.add_force_menu = AddForceMenu(self.parent)
        self.add_force_menu.display = False
        self.add_force_menu.x = 80
        self.add_force_menu.top = 70

    def add_bt_function(self):
        self.parent.show_options()

    def force_bt_function(self):
        self.add_force_menu.display = True
    
    def draw(self, offset_x=0, offset_y=0):
        self.draw_content(self.x + offset_x, self.y + offset_y)
