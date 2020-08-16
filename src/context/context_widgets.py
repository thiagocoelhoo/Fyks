import warnings

import pyglet

from ui import Frame, Button, Entry, Label, Subwindow
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
        label_x.lab.color = (190, 190, 190, 255)
        label_x.text = 'x'
        self.entry_x = Entry(40, 0, 140, 30, self.frame)
        self.entry_x.text = '0.0'
        self.entry_x.top = 20

        label_y = Label(20, 0, 0, 0, parent=self.frame)
        label_y.top = 80
        label_y.lab.color = (190, 190, 190, 255)
        label_y.text = 'y'
        self.entry_y = Entry(40, 0, 140, 30, self.frame)
        self.entry_y.top = 60
        self.entry_y.text = '0.0'

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
        try:
            x = float(self.entry_x.text)
            y = float(self.entry_y.text)
        except:
            warnings.warn('Warning: Error on float conversion.')
            return 1

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
        label_x.lab.color = (190, 190, 190, 255)
        label_x.text = 'x'
        self.entry_x = Entry(40, 0, 140, 30, self.frame)
        self.entry_x.text = '0.0'
        self.entry_x.top = 20

        label_y = Label(20, 0, 0, 0, parent=self.frame)
        label_y.top = 80
        label_y.lab.color = (190, 190, 190, 255)
        label_y.text = 'y'
        self.entry_y = Entry(40, 0, 140, 30, self.frame)
        self.entry_y.top = 60
        self.entry_y.text = '0.0'

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
        try:
            x = float(self.entry_x.text)
            y = float(self.entry_y.text)
        except:
            warnings.warn('Warning: Error on float conversion.')
            return 1

        for rb in self.parent.context.selected:
            rb.add_force(x, y)

        self.display = False


class RigidbodyInfoWindow(Subwindow):
    def __init__(self, parent):
        super().__init__(0, 0, 200, 155,
        title='Rb info', parent=parent)
        self.build()

    def build(self):
        label_x = Label(20, 0, 0, 0, parent=self.frame)
        label_x.top = 40
        label_x.lab.color = (190, 190, 190, 255)
        label_x.text = 'x'
        self.entry_x = Entry(40, 0, 140, 30, self.frame)
        self.entry_x.text = '0.0'
        self.entry_x.top = 20

        label_y = Label(20, 0, 0, 0, parent=self.frame)
        label_y.top = 80
        label_y.lab.color = (190, 190, 190, 255)
        label_y.text = 'y'
        self.entry_y = Entry(40, 0, 140, 30, self.frame)
        self.entry_y.top = 60
        self.entry_y.text = '0.0'

        self.submit_bt = Button(
            x=20,
            y=20,
            w=160,
            h=30,
            parent=self.frame,
            text='Ok'
        )

        self.display = False


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
