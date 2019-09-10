import os

import core
from core.camera import Camera
from core.rigidbody import RigidBody

core.init()
from ui import Button, Entry, Label, Frame, GraphicFrame, SubWindow, OptionsList
from application.simulationframe import SimulationFrame
from application.application import App

width = 1366
height = 738

os.environ['SDL_VIDEO_WINDOW_POS'] = f'0, 30'


class MainViewFrame(Frame):
    def __init__(self):
        super().__init__((0, 0), (width, height))
        content_frame = SimulationFrame((0, 0), (1166, 738))
        content_frame.color = (200, 200, 200)
        content_frame.bg_color = (10, 10, 10)
        content_frame.master = self

        options_frame = Frame((1166, 0), (200, 738))
        options_frame.color = (200, 200, 200)
        options_frame.bg_color = (220, 220, 220)
        options_frame.master = self
        
        options_frame['del_comp_bt'] = Button((20, 165), (100, 25), text='del', func=self.del_comp)
        
        options_frame['ax_entry'] = Entry('acceleration x', (20, 265), (160, 25))
        options_frame['ay_entry'] = Entry('acceleration y', (20, 315), (160, 25))
        options_frame['vx_entry'] = Entry('velocity x', (20, 365), (160, 25))
        options_frame['vy_entry'] = Entry('velocity y', (20, 415), (160, 25))
        options_frame['apply_bt'] = Button((20, 465), (100, 25), text='apply', func=self.apply_comp_acc)

        options_frame['run_time_entry'] = Entry('time', (20, 565), (160, 25))
        options_frame['run_pause_bt'] = Button((20, 615), (100, 25), text='run/pause', func=self.pause_run)
        
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

    def apply_comp_acc(self):
        master = self.widgets['content_frame']
        comp = master.selected
        
        try:
            ax = int(self.widgets['options_frame'].widgets['ax_entry'].text or '0')
            ay = -int(self.widgets['options_frame'].widgets['ay_entry'].text or '0')
            vx = int(self.widgets['options_frame'].widgets['vx_entry'].text or '0')
            vy = -int(self.widgets['options_frame'].widgets['vy_entry'].text or '0')
            comp.ax, comp.ay = (ax, ay)
            comp.vx, comp.vy = (vx, vy)
        except Exception as e:
            print(e)

    def show_comp_menu(self):
        comp = list(self.widgets['content_frame'].selection)[0]
        master = self.widgets['content_frame']
        
        frame_pos = (comp.x - master.cam.area.x - 125, comp.y - master.cam.area.y + 30)
        frame = Frame(frame_pos, (250, 40))
        frame.color = (255, 60, 0)
        frame['obj_pos_label'] = Label(f'x -> {comp.x}; y -> {comp.y}', (10, 10))
        
        master['comp_view'] = frame
    
    def add_comp(self):
        try:
            x = int(self.widgets['options_frame'].widgets['x_pos_entry'].text)
            y = int(self.widgets['options_frame'].widgets['y_pos_entry'].text)
            comp = RigidBody((x, y), (0, 0), (0, 0))
            self.widgets['content_frame'].add_component(comp)
        except Exception as e:
            print('Error!', e)
    
    def del_comp(self):
        comp = self.widgets['content_frame'].selected
        if comp:
            content_frame = self.widgets['content_frame']
            content_frame.selected = None
            content_frame.components.remove(comp)
            if 'obj_data_frame' in content_frame.widgets:
                content_frame.remove_widget('obj_data_frame')
            

if __name__ == "__main__":
    app = App(width, height)
    app.views['main'] = MainViewFrame()
    app.current_view = 'main'
    app.run()
