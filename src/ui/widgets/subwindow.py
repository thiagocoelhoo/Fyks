import pyglet
from pyglet import gl

# from ui import Frame, Button, Iconbutton, Label, Widget
from ui import widgets
import graphicutils as gu
from app import colors

close_icon = pyglet.image.load('assets/close_icon.png')


class Bar(widgets.Widget):
    def __init__(self, x, y, w, h, parent, caption):
        super().__init__(x=x, y=y, w=w, h=h, parent=parent)
        self.background_color = colors.SUBWINDOW_BAR_COLOR
        self.caption = caption
        self.init_ui()
    
    def init_ui(self):
        """
        Set widgets
        """

        # Caption label
        self.caption_label = widgets.Label(x=4, y=2, w=0, h=0)
        self.caption_label.font_size = 14
        self.caption_label.text = self.caption
        self.caption_label.lab.color = (130, 130, 130, 255)
        
        # Close button
        self.close_bt = widgets.Iconbutton(
            x=self.width - 18, y=2,
            w=16, h=16,
            image=close_icon,
            parent=self,
            command=self.parent.close
        )
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.close_bt.on_mouse_release(x, y, button, modifiers)
        if self.pressed:
            self.pressed = False
    
    def draw(self, offset_x, offset_y):
        x = self.x + offset_x
        y = self.y + offset_y

        gl.glColor4f(*self.background_color)
        gu.draw_rect(x, y,self.w, self.h, gl.GL_QUADS)
        
        self.caption_label.draw(x, y)
        self.close_bt.draw(x, y)


class Subwindow(widgets.Frame):
    def __init__(self, x, y, w, h, caption, parent):
        super().__init__(x=x, y=y, w=w, h=h + 20, parent=parent)
        self.caption = caption
        self.bar_height = 20
        self.bar_color = colors.SUBWINDOW_BAR_COLOR
        self.background_color = colors.SUBWINDOW_BACKGROUND_COLOR
        self.border_color = (0, 0, 0, 0.5)
        self.move = False
        
        self.init_ui()

    def init_ui(self):
        self.bar = Bar(
            x=0, y=self.height - self.bar_height, 
            w=self.width, 
            h=self.bar_height, 
            parent=self, 
            caption=self.caption
        )
        self.frame = widgets.Frame(0, 0, self.width, self.height - self.bar_height)
        self.frame.color = self.background_color
        self.frame.border_color = (0, 0, 0, 0)
        self.children = [self.bar, self.frame]
    
    def resize(self, w, h):
        self.width = w
        self.height = h + self.bar_height
        self.frame.height = h
        self.frame.width = w
        self.bar.width = w
    
    def show(self):
        self.close()
        self.is_visible = True

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        if self.bar.pressed:
            self.x += dx
            self.y += dy

    def close(self):
        self.is_visible = False
        for widget in self.children:
            widget.pressed = False
        for widget in self.frame.children:
            widget.pressed = False
    
    def draw(self, offset_x=0, offset_y=0):
        x = self.x + offset_x
        y = self.y + offset_y
        self.bar.draw(x, y)
        self.frame.draw(x, y)
        gl.glColor4f(*self.border_color)
        gu.draw_rect(x, y, self.w, self.h, gl.GL_LINE_LOOP)

    def update(self, dt):
        self.frame.update(dt)