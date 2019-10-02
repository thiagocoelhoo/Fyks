import os

import core
core.init()
from core.rigidbody import RigidBody
from ui import Button, Entry, Label, Frame, SubWindow, OptionsList, ItemList
from application.contextframe import ContextFrame
from application.base import App

width = 1366
height = 738

os.environ['SDL_VIDEO_WINDOW_POS'] = f'0, 30'
core.set_theme("white")


class MainViewFrame(Frame):
    def __init__(self):
        super().__init__((0, 0), (width, height))
        content_frame = ContextFrame(self, (0, 0), (1166, 738))
        options_frame = Frame((1166, 0), (200, 738))
        options_frame.master = self
        
        options_frame['run_time_entry'] = Entry('Time', (20, 35), (160, 25))
        options_frame['run_pause_bt'] = Button((20, 85), (100, 25), text='run/pause', func=self.pause_run)
        vector_list = OptionsList((20, 150), (160, 300))
        vector_list.close_after = False
        vector_list.bg_color = (150, 150, 180)
        options_frame['vectors_list'] = vector_list

        self.widgets['options_frame'] = options_frame
        self.widgets['content_frame'] = content_frame
    
    def pause_run(self):
        master = self.widgets['content_frame']
        master.toggle_pause()
        
        try:
            master.max_time = int(self.widgets['options_frame'].widgets['run_time_entry'].text or '0')
        except Exception as e:
            print(e)
        
        if not 'status_label' in list(master.widgets.keys()):
            status_label = Label('', (20, 20))
            status_label.color = (200, 0, 0)
            master.widgets['status_label'] = status_label

        master.widgets['status_label'].text = f'paused: {master.paused}'
    
    def del_comp(self):
        for comp in self.widgets['content_frame'].selection.copy():
            content_frame = self.widgets['content_frame']
            content_frame.components.remove(comp)
            self.widgets['content_frame'].selection.remove(comp)
            if 'obj_data_frame' in content_frame.widgets:
                content_frame.remove_widget('obj_data_frame')


if __name__ == "__main__":
    app = App(width, height)
    mframe = MainViewFrame()
    app.views['main'] = mframe
    app.current_view = 'main'
    app.run()
