import pyglet
from pyglet import gl
from pyglet.window import key

import graphicutils as gu
from app import colors
from ui import Widget, Slidebar, Iconbutton, Label
from context.context_wrapper import ContextWrapper
from constants import *

pause_icon = pyglet.image.load('assets/pause_icon.png')
play_icon = pyglet.image.load('assets/play_icon.png')
rec_icon = pyglet.image.load('assets/rec_icon.png')

ctx_wrapper = ContextWrapper(0, 0)


class Timeline(Widget):
    def __init__(self, x, y, parent):
        super().__init__(x, y, w=parent.w - 104, h=24, parent=parent)
        self.mode = PAUSE
        self.frame = 0
        self.frames = []
        self.init_ui()
    
    def init_ui(self):
        self.pause_bt = Iconbutton(
            x=self.x, y=self.y,
            w=16, h=16, 
            image=pause_icon, 
            parent=self,
            command=ctx_wrapper.toggle_pause)
        
        self.rec_bt = Iconbutton(
            x=self.x + 20, y=self.y, 
            w=16, h=16,
            image=rec_icon,
            parent=self,
            command=self.toggle_rec)

        self.slidebar = Slidebar(
            x=self.x + 40, y=self.y, 
            w=self.parent.w - 118, h=16, 
            parent=self)
        
        self.slidebar.background_color = colors.TIMELINE_BACKGROUND_COLOR
        self.slidebar.inside_color = colors.TIMELINE_COLOR
        self.slidebar.value = 0

        self.clock_label = Label(
            x=self.slidebar.x + 24, y=self.slidebar.y + 24, 
            w=0, h=0,
            parent=self)
        
        self.clock = 0
        self.clock_label.text = "00:00"
        self.clock_label.lab.color = (220, 220, 220, 255)

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        self.slidebar.on_mouse_press(x, y, button, modifiers)
        self.pause_bt.on_mouse_press(x, y, button, modifiers)
        self.rec_bt.on_mouse_press(x, y, button, modifiers)
    
    def on_mouse_release(self, x, y, button, modifiers):
        super().on_mouse_release(x, y, button, modifiers)
        self.slidebar.on_mouse_release(x, y, button, modifiers)
        self.pause_bt.on_mouse_release(x, y, button, modifiers)
        self.rec_bt.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.slidebar.pressed:
            self.slidebar.on_mouse_drag(x, y, dx, dy, buttons, modifiers)
            frame = int(self.slidebar.value * len(self.frames))
            self.set_frame(frame)
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.G:
            if self.mode == REC:
                self.mode = PAUSE
                wrapper._running = False
            else:
                self.mode = REC
                wrapper._running = True
    
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
            ctx_wrapper._set_objects_data(self.frames[frame])
    
    def write_frame(self):
        self.frames.append(tuple(ctx_wrapper._get_objects_data()))
    
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
    
    def draw(self, offset_x, offset_y):
        if ctx_wrapper._running:
            self.pause_bt.image = pause_icon
        else:
            self.pause_bt.image = play_icon
        
        self.slidebar.draw(offset_x, offset_y)
        self.pause_bt.draw(offset_x, offset_y)
        self.rec_bt.draw(offset_x, offset_y)
        self.clock_label.draw(offset_x, offset_y)
