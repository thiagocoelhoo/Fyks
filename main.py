import os

import numpy as np
import pygame
import pygame.gfxdraw

import core
from core.camera import Camera
from core.rigidbody import RigidBody

core.init()
from ui import Button, Entry, Label, Frame, GraphicFrame, SubWindow
from application.simulationframe import SimulationFrame

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

        content_frame['graphic'] = GraphicFrame((20, 500), (380, 208))
        # content_frame.widgets['graphic'].bg_color = (220, 220, 220)
        
        content_frame['lalala'] = SubWindow((100, 100), 400, 300)

        options_frame = Frame((1166, 0), (200, 738))
        options_frame.color = (200, 200, 200)
        options_frame.bg_color = (220, 220, 220)
        options_frame.master = self

        options_frame['x_pos_entry'] = Entry('pos x', (20, 25), (160, 25))
        options_frame['y_pos_entry'] = Entry('pos y', (20, 75), (160, 25))
        options_frame['add_comp_bt'] = Button((20, 120), (100, 25), text='add', func=self.add_comp)
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
        comp = master.last_selected
        
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
        comp = self.widgets['content_frame'].selection[0]
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
        comp = self.widgets['content_frame'].last_selected
        if comp:
            self.widgets['content_frame'].last_selected = None
            self.widgets['content_frame'].components.remove(comp)
    
    def draw(self, surface):
        super().draw(surface)


class App:
    def __init__(self):
        self.surface = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.mouse = core.get_mouse()
        self.views = {
            'main': MainViewFrame(),
        }
        self.current_view = 'main'
        self.running = False
        self.dt = 0

        self.eventhandler = core.get_eventhandler()
        self.eventhandler.add_handler(pygame.QUIT, self.on_quit)
        self.eventhandler.add_handler(pygame.KEYDOWN, self.on_keydown)
        self.eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousebtndown)

    def on_quit(self, event):
        self.running = False
    
    def on_keydown(self, event):
        for entry in Entry.all():
            if entry.active:
                entry.on_keydown(event)
                return 0
    
    def on_mousebtndown(self, event):
        pass
    
    def on_mousebtnup(self, event):
        pass
    
    def run(self):
        self.running = True
        while self.running:
            self.eventhandler.update()
            self.surface.fill((0, 0, 0))
            self.mouse.update()
            self.views[self.current_view].update(self.dt)
            self.views[self.current_view].draw(self.surface)  
            pygame.display.update()
            self.dt = self.clock.tick(120) / 1000
        pygame.quit()


if __name__ == "__main__":
    app = App()
    app.run()
