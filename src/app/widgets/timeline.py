import pyglet
from pyglet import gl
from pyglet.window import key

import graphicutils as gu
from app import colors
from ui import widgets
from core.context_wrapper import ContextWrapper
from constants import *

pause_icon = pyglet.image.load('assets/pause_icon.png')
play_icon = pyglet.image.load('assets/play_icon.png')
rec_icon = pyglet.image.load('assets/rec_icon.png')

ctx_wrapper = ContextWrapper(0, 0)


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
            image=pause_icon, 
            command=ctx_wrapper.toggle_pause)
        self.pause_bt.max_width = 25
        
        self.rec_bt = widgets.Iconbutton(
            x=0, y=2, 
            w=16, h=16, 
            image=rec_icon, 
            command=self.toggle_rec)
        self.rec_bt.max_width = 25
        
        self.slidebar = widgets.Slidebar(x=0, y=0, w=0, h=16)
        self.slidebar.background_color = colors.TIMELINE_BACKGROUND_COLOR
        self.slidebar.inside_color = colors.TIMELINE_COLOR
        self.slidebar.value = 0
        self.slidebar.max_height = 16

        self.clock_label = widgets.Label(0, 0, 0, 0)
        self.clock_label.lab.color = (220, 220, 220, 255)
        self.clock_label.text = "00:00"

        self.add(self.pause_bt)
        self.add(self.rec_bt)
        self.add(self.slidebar)
        # self.add(self.clock_label)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.slidebar.pressed:
            self.slidebar.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
            frame = int(self.slidebar.value * len(self.frames))
            self.set_frame(frame)
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.G:
            if self.mode == REC:
                self.mode = PAUSE
                ctx_wrapper._running = False
            else:
                self.mode = REC
                ctx_wrapper._running = True
    
    def toggle_rec(self):
        if self.mode != REC:
            self.mode = REC
            self.frames = self.frames[:self.frame]
            self.slidebar.value = 1
        else:
            self.mode = PAUSE
        ctx_wrapper.toggle_pause()
    
    def set_frame(self, frame):
        if -1 < frame < len(self.frames):
            self.frame = frame
            ctx_wrapper.set_data(self.frames[frame])
    
    def write_frame(self):
        self.frames.append(tuple(ctx_wrapper.get_data()))
    
    def resize(self, width, height):
        super().resize(width, height)
    
    def update(self, dt):
        if self.mode == REC:
            self.write_frame()
        elif self.mode == PLAY and self.frames:         
            self.slidebar.value = self.frame / len(self.frames)
        
        if ctx_wrapper._running:
            self.clock += dt
            m = int(self.clock // 60)
            s = int(self.clock % 60)
            self.clock_label.text = f'{m:>02}:{s:>02}'
            
        if ctx_wrapper._running:
            self.pause_bt.image = pause_icon
        else:
            self.pause_bt.image = play_icon
