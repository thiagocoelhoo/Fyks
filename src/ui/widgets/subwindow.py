import pyglet
from pyglet import gl

# from ui import Frame, Button, Iconbutton, Label, Widget
from ui import widgets
import graphicutils as gu
from app import colors

close_icon = pyglet.image.load('assets/close_icon.png')


class Bar(widgets.Frame):
    def __init__(self, x, y, w, h, parent, caption):
        super().__init__(x=x, y=y, w=w, h=h, parent=parent)
        self.color = colors.SUBWINDOW_BAR_COLOR
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
        self.add(self.caption_label)
        self.add(self.close_bt)
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.close_bt.on_mouse_release(x, y, button, modifiers)
        if self.pressed:
            self.pressed = False


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

        self.frame = widgets.Frame(
            x=0, y=0, 
            w=self.width, 
            h=self.height - self.bar_height)
        self.frame.color = self.background_color
        self.frame.border_color = (0, 0, 0, 0)
        self.children = [self.bar, self.frame]

        self.add(self.bar)
        self.add(self.frame)
    
    def resize(self, width, height):
        self.width = width
        self.height = height + self.bar_height
        self.frame.height = height
        self.frame.width = width
        self.bar.width = width
    
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
        for widget in self.elements:
            widget.pressed = False
        for widget in self.frame.elements:
            widget.pressed = False
    
    def draw(self):
        self.bar.draw()
        self.frame.draw()
        self.update_viewport()
        gl.glColor4f(*self.border_color)
        gu.draw_rect(1, 0, self.width-1, self.height-1, gl.GL_LINE_LOOP)

    def update(self, dt):
        self.frame.update(dt)