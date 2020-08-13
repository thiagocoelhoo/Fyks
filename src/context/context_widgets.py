import warnings

import pyglet

from ui import Frame, Button, Entry, Label
from core.rigidbody import RigidBody



class ContextOptionsMenu(Frame):
    def __init__(self, parent):
        super().__init__(0, 0, 200, 155, parent=parent)
        self.build()
    
    def build(self):
        label_x = Label(20, 0, 0, 0, parent=self)
        label_x.top = 40
        label_x.lab.color = (190, 190, 190, 255)
        label_x.text='x'
        self.entry_x = Entry(40, 0, 140, 30, self)
        self.entry_x.text = '0.0'
        self.entry_x.top = 20

        label_y = Label(20, 0, 0, 0, parent=self)
        label_y.top = 80
        label_y.lab.color = (190, 190, 190, 255)
        label_y.text='y'
        self.entry_y = Entry(40, 0, 140, 30, self)
        self.entry_y.top = 60
        self.entry_y.text = '0.0'

        self.submit_bt = Button(
            x=20,
            y=20,
            w=160,
            h=30,
            parent=self,
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


class AddForceMenu(Frame):
    def __init__(self, parent):
        super().__init__(0, 0, 200, 155, parent=parent)
        self.build()
    
    def build(self):
        label_x = Label(20, 0, 0, 0, parent=self)
        label_x.top = 40
        label_x.lab.color = (190, 190, 190, 255)
        label_x.text='x'
        self.entry_x = Entry(40, 0, 140, 30, self)
        self.entry_x.text = '0.0'
        self.entry_x.top = 20

        label_y = Label(20, 0, 0, 0, parent=self)
        label_y.top = 80
        label_y.lab.color = (190, 190, 190, 255)
        label_y.text='y'
        self.entry_y = Entry(40, 0, 140, 30, self)
        self.entry_y.top = 60
        self.entry_y.text = '0.0'

        self.submit_bt = Button(
            x=20,
            y=20,
            w=160,
            h=30,
            parent=self,
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


class ToolBox(Frame):
    def __init__(self, parent):
        super().__init__(0, 0, 80, parent.context.h, parent)
        self.color = (0.05, 0.05, 0.15, 0.4)
        self.build()
    
    def build(self):
        self.add_bt = Button(
            x=10,
            y=0,
            w=60,
            h=40,
            parent=self,
            text='Add',
            command=self.add_bt_function)
        self.add_bt.null_color = (0.05, 0.05, 0.15, 0.4)
        self.add_bt.color = (0.05, 0.05, 0.15, 0.4)
        self.add_bt.border_color = (0.3, 0.3, 0.8, 0.5)
        self.add_bt.border_radius = 0
        self.add_bt.top = 20
        
        self.force_bt = Button(
            x=10, 
            y=0, 
            w=60, 
            h=40,
            parent=self,
            text='Force',
            command=self.force_bt_function)
        self.force_bt.null_color = (0.05, 0.05, 0.15, 0.4)
        self.force_bt.color = (0.05, 0.05, 0.15, 0.4)
        self.force_bt.border_color = (0.3, 0.3, 0.8, 0.5)
        self.force_bt.border_radius = 0
        self.force_bt.top = 70

        self.add_force_menu = AddForceMenu(self.parent)
        self.add_force_menu.display = False
        self.add_force_menu.x = 80
        self.add_force_menu.top = 70
    
    def add_bt_function(self):
        self.parent.show_options()
    
    def force_bt_function(self):
        self.add_force_menu.display = True

    def draw(self, offset_x, offset_y):
        super().draw(offset_x, offset_y)
        rect = (1, 1, 80, 1, 80, self.h - 2, 1, self.h -2)
        pyglet.gl.glColor4f(0.3, 0.3, 0.8, 0.5)
        pyglet.graphics.draw(
            4, pyglet.gl.GL_LINE_LOOP,
            ('v2f', rect)
        )