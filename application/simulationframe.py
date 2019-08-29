import pygame
import pygame.gfxdraw

from ui import Frame, Button, Label
import core
from core.camera import Camera

mouse = core.get_mouse()


class SimulationFrame(Frame):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.mode = 'None'
        self.components = []
        self.selection = []
        self.last_selected = None
        self.selection_box = None
        self.cam = Camera((-size[0]/2, -size[1]/2), size)
        self.autoclear = False
        self.paused = True
        self.zoom = 1
        
        self.max_time = 0

        self.time  = 0
        self.x_data = []
        self.y_data = []

        self.eventhandler = core.get_eventhandler()
        self.eventhandler.add_handler(pygame.MOUSEMOTION, self.on_mousemotion)
        
    def toggle_pause(self):
        self.paused = not self.paused
    
    def add_component(self, comp):
        self.components.append(comp)
    
    def draw_selection_box(self):
        if self.selection_box:
            pygame.gfxdraw.rectangle(self.surface, self.selection_box, (100, 150, 255, 200))
            pygame.gfxdraw.box(self.surface, self.selection_box, (100, 150, 255, 50))
    
    def draw_components(self):
        for comp in self.components:
            if self.cam.collide(comp):
                self.cam.render(self.surface, comp)
    
    def draw_overlay(self):
        if self.last_selected:
            compx = self.last_selected.x - self.cam.area.x - 20
            compy = self.last_selected.y - self.cam.area.y - 20
            pygame.gfxdraw.rectangle(self.surface, [compx, compy, 41, 41], (0, 255, 0))

        for comp in self.selection:    
            compx = comp.x - self.cam.area.x - 20
            compy = comp.y - self.cam.area.y - 20
            pygame.gfxdraw.rectangle(self.surface, [compx, compy, 41, 41], (0, 255, 0))
    
    def show_options(self, mpos):
        menu = Frame(mpos, (200, 100))
        menu['add'] = Button((0, 0), (200, 25), 'add')
        menu['exclude'] = Button((0, 25), (200, 25), 'exclude')
        menu['view'] = Button((0, 50), (200, 25), 'view')
        menu['exit'] = Button((0, 75), (200, 25), 'exit')
        
        self.widgets['options_menu'] = menu 
    
    def on_mousemotion(self, event):
        if self.is_inside(event.pos):
            pass
    
    def update(self, dt):
        super().update(dt)

        rx, ry = mouse.rel
        mx, my = mouse.pos
        key = pygame.key.get_pressed()

        '''
        #=====================ZOOM=======================

        if key[pygame.K_UP] and self.cam.zoom < 5.0:
            self.zoom += 0.1
            self.cam.zoom += 0.1
        if key[pygame.K_DOWN] and self.cam.zoom > 0.3:
            self.cam.zoom -= 0.1
        '''

        if self.max_time and self.time >= self.max_time:
            self.paused = True
        
        if not self.paused and self.last_selected and self.last_selected.vx:
            self.time += dt
            self.x_data.append(self.time)
            self.y_data.append(self.last_selected.vx)
            w = max(self.x_data) - min(self.x_data) + 1
            h = max(self.y_data) - min(self.y_data) + 1
            y = [i/h*200 for i in self.y_data]
            x = [j/w*200 for j in self.x_data]

            self.widgets['graphic'].plot(x, y)
        self.widgets['graphic'].update(dt)

        if self.is_hover():
            if mouse.pressed[0]:
                if key[pygame.K_LCTRL]:
                    self.cam.area.x -= rx
                    self.cam.area.y -= ry
                elif key[pygame.K_LSHIFT]:
                    if self.selection_box is not None:
                        self.selection_box.w = mx - self.selection_box[0]
                        self.selection_box.h = my - self.selection_box[1]
                    else:
                        self.selection_box = pygame.Rect([mx, my, 0, 0])
                else:
                    for obj in self.selection:
                        obj.x += rx
                        obj.y += ry
            elif mouse.pressed[2]:
                if self.selection:
                    self.last_selected = self.selection[-1]
                else:
                    self.show_options((mx - 5, my - 5))
            elif self.selection_box:
                self.selection_box = None
        
        if self.selection and (mouse.pressed[0] or key[pygame.K_LSHIFT]):
            master = self.master
            master.show_comp_menu()
        elif self.widgets.get('comp_view'):
            del self.widgets['comp_view']
        
        if self.last_selected:
            # if 'comp_info_frame' in list(self.master.widgets['options_frame'].widgets.keys()):
            if 'comp_info_frame' in list(self.widgets.keys()):
                # frame = self.master.widgets['options_frame'].widgets['comp_info_frame']
                frame = self.widgets['comp_info_frame']
                frame.widgets['velocity_label'].text = f'velocity:{self.last_selected.vx:.2f}; {self.last_selected.vy:.2f}'
                frame.widgets['acceleration_label'].text = f'acceleration:{self.last_selected.ax:.2f}; {self.last_selected.ay:.2f}'
                frame.widgets['position_label'].text = f'position:{self.last_selected.x:.2f}; {self.last_selected.y:.2f}'
            else:
                frame = Frame((20, 40), (300, 150))
                frame.color = (100, 100, 100)
                frame.bg_color = (220, 220, 220)
                frame['velocity_label'] = Label(f'velocity:{self.last_selected.vx:.2f}; {self.last_selected.vy:.2f}', (20, 20))
                frame.widgets['velocity_label'].color = (80, 80, 80)
                frame['acceleration_label'] = Label(f'acceleration:{self.last_selected.ax:.2f}; {self.last_selected.ay:.2f}', (20, 50))
                frame.widgets['acceleration_label'].color = (80, 80, 80)
                frame['position_label'] = Label(f'position:{self.last_selected.x:.2f}; {self.last_selected.y:.2f}', (20, 80))
                frame.widgets['position_label'].color = (80, 80, 80)
                frame['close_bt'] = Button((20, 110), (100, 25), text='close')
                frame.master = self
                # self.master.widgets['options_frame'].widgets['comp_info_frame'] = frame
                self.widgets['comp_info_frame'] = frame

        for comp in self.components:
            if self.cam.collide(comp):
                dx = (comp.x - mx - self.cam.area.x)
                dy = (comp.y - my - self.cam.area.y)
                d = (dx**2 + dy**2)**0.5
                comp_rect = ((comp.x - self.cam.area.x, comp.y - self.cam.area.y), comp.size)
                if self.selection_box is not None:
                    if self.selection_box.colliderect(comp_rect):
                        self.selection.append(comp)
                    elif comp in self.selection:
                        self.selection.remove(comp)
                elif d <= 20:
                    self.selection.clear()
                    self.selection.append(comp)
                elif comp in self.selection:
                    self.selection.remove(comp)
            
            if not self.paused:
                comp.update(dt)
    
    def draw(self, surface):
        self.surface.fill(self.bg_color)
        self.cam.draw_grid(self.surface)
        self.cam.draw_axes(self.surface)
        self.draw_overlay()
        self.draw_components()
        self.draw_selection_box()
        
        super().draw(surface)
