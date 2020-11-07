import pyglet
from pyglet import gl

from ui import widgets
import graphicutils as gu

close_icon = pyglet.image.load('assets/close_icon.png')


class Item(widgets.Widget):
    def __init__(self, x, y, w, h, parent, text):
        super().__init__(x, y, w, h, parent)
        self.background_color = (1, 1, 1, 0.2)
        self.text = text
        self.selected = False
        self.init_ui()
    
    def init_ui(self):
        self.label = Label(2, 2, 0, 0, self)
        self.label.text = self.text
        self.label.lab.color = (200, 200, 200, 255)
        self.close_bt = Iconbutton(
            x=self.w - 18, y=2,
            w=16, h=16,
            image=close_icon,
            parent=self,
            command=self.delete
        )
    
    def delete(self):
        self.parent.remove_item(self)
    
    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        if self.pressed:
            self.parent.select_item(self)

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def draw(self, offset_x, offset_y):
        x = self.x + offset_x
        y = self.y + offset_y
        
        if self.pressed:
            gl.glColor4f(*self.background_color)
            gu.draw_rect(x, y, self.w, self.h, gl.GL_QUADS)
        
        self.label.draw(x, y)
        self.close_bt.draw(x, y)


class List(widgets.Frame):
    def __init__(self, x, y, w, h, parent):
        super().__init__(x, y, w, h, parent)
        self.background_color = (1, 1, 1, 0.05)

    def add_item(self, name):
        item = Item(
            x=0, y=0,
            w=self.w, h=20,
            text=name,
            parent=self
        )
        item.top = (len(self.children) - 1) * 20

    def on_mouse_release(self, x, y, button, modifiers):
        super().on_mouse_release(x, y, button, modifiers)

    def select_item(self, item):
        for i in self.children:
            i.selected = False
        item.selected = True

    def remove_item(self, item):
        self.children.remove(item)
    
    def draw(self, offset_x, offset_y):
        x = self.x + offset_x
        y = self.y + offset_y
        
        gl.glColor4f(*self.background_color)
        gu.draw_rect(x, y, self.w, self.h, gl.GL_QUADS)

        for item in self.children:
            item.draw(x, y)
