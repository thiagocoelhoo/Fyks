import pyglet
from pyglet.window import key

from app import colors
from ui import widgets
from constants import *

pause_icon = pyglet.image.load('assets/pause_icon.png')
play_icon = pyglet.image.load('assets/play_icon.png')
rec_icon = pyglet.image.load('assets/rec_icon.png')


class Timeline(widgets.Layout):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, w=0, h=24, orientation="vertical")
        self.mode = PAUSE
        self.frame = 0
        self.frames = []
        self.clock = 0
        self.init_ui()
        self.color = (0, 0, 0, 0)
    
    def init_ui(self):
        self.pause_bt = widgets.Iconbutton(
            x=0, y=2,
            w=16, h=16, 
            image=pause_icon)
        self.pause_bt.max_width = 25
        
        self.rec_bt = widgets.Iconbutton(
            x=0, y=2, 
            w=16, h=16, 
            image=rec_icon)
        self.rec_bt.max_width = 25
        
        self.slidebar = widgets.Slidebar(x=0, y=0, w=0, h=16)
        self.slidebar.background_color = colors.TIMELINE_BACKGROUND_COLOR
        self.slidebar.inside_color = colors.TIMELINE_COLOR
        self.slidebar.value = 0
        self.slidebar.max_height = 16

        self.add(self.pause_bt)
        self.add(self.rec_bt)
        self.add(self.slidebar)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.slidebar.pressed:
            self.slidebar.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    
    def update(self, dt):
        pass