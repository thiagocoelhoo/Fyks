import pyglet
from pyglet import gl
from pyglet.window import key

from ui.widgets.widget import Widget
from ui.widgets.slidebar import Slidebar
from ui.widgets.iconbutton import Iconbutton
from app import colors
import graphicutils as gu
from context.context_wrapper import ContextWrapper

REC = 1
PLAY = 2
PAUSE = 3

pause_icon = pyglet.image.load('assets/pause_icon.png')
play_icon = pyglet.image.load('assets/play_icon.png')
rec_icon = pyglet.image.load('assets/rec_icon.png')

wrapper = ContextWrapper(0, 0)


class Timeline(Widget):
    def __init__(self, x, y, parent):
        super().__init__(x, y, w=parent.w - 104, h=16, parent=parent)
        self.value = 0
        self.mode = PAUSE
        
        self.pause_bt = Iconbutton(
            x=x, y=y, w=16, h=16, 
            image=pause_icon, 
            parent=self,
            command=wrapper.toggle_pause
        )
        
        self.slidebar = Slidebar(x + 20, y, parent.w - 104, 16, self)
        self.slidebar.background_color = colors.TIMELINE_BACKGROUND_COLOR
        self.slidebar.inside_color = colors.TIMELINE_COLOR
        self.slidebar.value = 0

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        self.pause_bt.on_mouse_press(x, y, button, modifiers)
    
    def on_mouse_release(self, x, y, button, modifiers):
        super().on_mouse_release(x, y, button, modifiers)
        self.pause_bt.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.slidebar.pressed = self.pressed
        self.slidebar.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.G:
            if self.mode == REC:
                self.mode = PAUSE
                wrapper._running = False
            else:
                self.mode = REC
                wrapper._running = True
    
    def update(self, dt):    
        if wrapper._running:
            self.value = 1
            if self.mode == REC:
                wrapper._write_frame()
    
    def draw(self, offset_x, offset_y):

        if wrapper._running:
            self.pause_bt.image = pause_icon
        else:
            self.pause_bt.image = play_icon
        
        self.slidebar.draw(offset_x, offset_y)
        self.pause_bt.draw(offset_x, offset_y)