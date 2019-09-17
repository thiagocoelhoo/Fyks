# frame de simulação de particulas (plano cartesiano)
import pygame
import pygame.gfxdraw

import core
from core.camera import Camera
from core.rigidbody import RigidBody, ForceField
from core.collisions import collide
from application.context import Context
from ui import (
    Frame,
    Button,
    Label,
    SubWindow,
    Entry,
    OptionsList,
)

mouse = core.get_mouse()


class ObjectDataFrame(SubWindow):
    def __init__(self, obj):
        super().__init__((20, 40), 300, 340, title="RigidBodyConfig")
        self.color = (100, 100, 100)
        self.autoclear = True

        self['velocity_entry_x'] = Entry("Velocity x", (20, 65), (100, 25))
        self.widgets['velocity_entry_x'].color = (80, 80, 80)
        self['velocity_entry_y'] = Entry("Velocity y", (160, 65), (100, 25))
        self.widgets['velocity_entry_y'].color = (80, 80, 80)

        self['acceleration_entry_x'] = Entry("Acceleration x", (20, 125), (100, 25))
        self.widgets['acceleration_entry_x'].color = (80, 80, 80)
        self['acceleration_entry_y'] = Entry("Acceleration y", (160, 125), (100, 25))
        self.widgets['acceleration_entry_y'].color = (80, 80, 80)
    
        self['force_entry_x'] = Entry("Force x", (20, 185), (100, 25))
        self.widgets['force_entry_x'].color = (80, 80, 80)
        self['force_entry_y'] = Entry("Force y", (160, 185), (100, 25))
        self.widgets['force_entry_y'].color = (80, 80, 80)

        self['position_entry_x'] = Entry("Position x", (20, 245), (100, 25))
        self.widgets['position_entry_x'].color = (80, 80, 80)
        self['position_entry_y'] = Entry("Position y", (160, 245), (100, 25))
        self.widgets['position_entry_y'].color = (80, 80, 80)

        self['close_bt'] = Button((40, 330), (100, 25), text='close', func=self.close)
        self['apply_bt'] = Button((160, 330), (100, 25), text='apply', func=lambda: self.apply(obj))

    def update_data(self, obj):
        try:
            acc_x_entry = self.widgets['acceleration_entry_x']
            if acc_x_entry.changed:
                self.widgets['force_entry_x'].text = f"{float(acc_x_entry.text) * obj.mass:.2f}"

            acc_y_entry = self.widgets['acceleration_entry_y']
            if acc_y_entry.changed:
                self.widgets['force_entry_y'].text = f"{float(acc_y_entry.text) * obj.mass:.2f}"

            force_x_entry = self.widgets['force_entry_x']
            if force_x_entry.changed:
                self.widgets['acceleration_entry_x'].text = f"{float(force_x_entry.text) / obj.mass:.2f}"
        
            force_y_entry = self.widgets['force_entry_y']
            if force_y_entry.changed:
                self.widgets['acceleration_entry_y'].text = f"{float(force_y_entry.text) / obj.mass:.2f}"
        
            self.bg_color = core.theme['frame-background-color']
        except:
            self.bg_color = core.theme['frame-background-color-error']

        if not self.widgets['velocity_entry_x'].active:
            self.widgets['velocity_entry_x'].text = f'{obj.vx:.2f}'
        if not self.widgets['velocity_entry_y'].active:
            self.widgets['velocity_entry_y'].text = f'{obj.vy:.2f}'
        
        '''
        if not self.widgets['force_entry_x'].active and self.widgets['acceleration_entry_x'].active:
            self.widgets['force_entry_x'].text = f'{float(acc_x_entry.text) * obj.mass:.2f}'
        if not self.widgets['force_entry_y'].active and self.widgets['acceleration_entry_y'].active:
            self.widgets['force_entry_y'].text = f'{float(acc_y_entry.text) * obj.mass:.2f}'
        
        if not self.widgets['position_entry_x'].active:
            self.widgets['position_entry_x'].text = f'{obj.x:.2f}'
        if not self.widgets['position_entry_y'].active:
            self.widgets['position_entry_y'].text = f'{obj.y:.2f}'
        '''

        if not self.widgets['position_entry_x'].active:
            self.widgets['position_entry_x'].text = f'{obj.x:.2f}'
        if not self.widgets['position_entry_y'].active:
            self.widgets['position_entry_y'].text = f'{obj.y:.2f}'
        
    def apply(self, obj):
        vx = self.widgets['velocity_entry_x'].text
        vy = self.widgets['velocity_entry_y'].text
        
        fx = self.widgets['force_entry_x'].text
        fy = self.widgets['force_entry_y'].text

        px = self.widgets['position_entry_x'].text
        py = self.widgets['position_entry_y'].text
        
        try:
            obj.vx = float(vx)
            obj.vy = float(vy)
            obj.apply_force((float(fx), float(fy)))
            obj.x = float(px)
            obj.y = float(py)

            self.bg_color = core.theme['frame-background-color']
        except:
            self.bg_color = (230, 210, 210)

    def close(self):
        self.master.remove_widget('obj_data_frame')


class SimulationFrame(Frame):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.context = Context(size)
        self.mode = 'None'
        self.autoclear = False
        
        self.paused = True
        self.max_time = 0

        self.selection = []
        self.__selected = None
        self.selection_box = None

        self.eventhandler = core.get_eventhandler()
        self.eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousedown)
        self.eventhandler.add_handler(pygame.MOUSEBUTTONUP, self.on_mouseup)
        self.eventhandler.add_handler(pygame.KEYDOWN, self.on_keydown)
        self.eventhandler.add_handler(pygame.KEYUP, self.on_keyup)
    
    @property
    def selected(self):
        return self.__selected
    
    @selected.setter
    def selected(self, value):
        self.show_object_options(value)
        self.__selected = value
    
    def toggle_pause(self):
        self.paused = not self.paused

    def show_options(self, mpos):
        options = OptionsList(mpos, (200, 125))
        options.set_options({
            'Add rigidbody': self.show_add_options,
            'Add forcefield': self.add_forcefield_mode,
            'Remove': self.remove_component,
            'Info': None,
            'Exit': None,
        })
        
        self.add_widget('options_menu', options)
    
    def show_add_options(self):
        frame = SubWindow(mouse.pos, 230, 185)
        frame.autoclear = True

        pos_x_entry = Entry("Position x", (10, 60), (100, 25))
        pos_y_entry = Entry("Position y", (120, 60), (100, 25))
        pos_x_entry.text = "0"
        pos_y_entry.text = "0"
        mass_entry = Entry("Mass", (10, 115), (100, 25), '10.0')

        frame["position_x_entry"] = pos_x_entry
        frame["position_y_entry"] = pos_y_entry
        frame["mass_entry"] = mass_entry

        add_func = lambda: self.add_object((int(frame.widgets['position_x_entry'].text), int(frame.widgets['position_y_entry'].text)), frame.widgets['mass_entry'].text)
        frame["add_button"] = Button((120, 180), (100, 25), "Add", func=add_func)
        self.widgets["add_options"] = frame

    def show_object_options(self, obj):
        if not 'obj_data_frame' in list(self.widgets.keys()):
            obj_data_frame = ObjectDataFrame(obj)
            obj_data_frame.master = self
            obj_data_frame.update_data(obj)
            self.widgets['obj_data_frame'] = obj_data_frame

    def add_forcefield_mode(self):
        self.mode = "forcefield-add"

    def add_object(self, position, mass):
        if "add_options" in list(self.widgets):
            self.remove_widget("add_options")
        
        obj = RigidBody(position, (0, 0), (0, 0), float(mass))
        self.context.add_object(obj) 

    def remove_component(self):
        pass
    
    def on_mousedown(self, event):
        if event.button == 3:
            self.show_options((event.pos[0] - 10, event.pos[1] - 10))

        if event.button == 1:
            if self.mode == 'forcefield-add':
                ff = ForceField(event.pos, (200, 200), (0.0, 0.0))
                self.add_component(ff)
                self.mode == 'forcefield-edit'
            elif self.selection:
                self.selected = self.selection[-1]
    
    def on_mouseup(self, event):
        if event.button == 1 and self.mode == "move":
            self.mode = "None"
    
    def on_keydown(self, event):
        if event.key == pygame.K_m:
            self.mode = "move"
        elif event.key == pygame.K_LCTRL:
            self.mode = "move_spc"
        
    def on_keyup(self, event):
        if event.key == pygame.K_LCTRL:
            self.mode = "None"
    
    def update(self, dt):
        super().update(dt)

        rx, ry = mouse.rel
        mx, my = mouse.pos

        if self.max_time and self.context.time >= self.max_time:
            self.paused = True

        if self.is_mouse_over():
            if mouse.pressed[0]:
                if self.mode == "move":
                    for obj in self.selection:
                        obj.x += rx
                        obj.y += ry
                elif self.mode == "move_spc":
                    self.context.cam.area.x -= rx
                    self.context.cam.area.y -= ry
                elif self.mode == 'None':
                    for k in self.widgets:
                        if self.widgets[k].active:
                            self.selection_box = None
                            break
                    else:
                        if self.selection_box is not None:
                            self.selection_box.w = mx - self.selection_box[0]
                            self.selection_box.h = my - self.selection_box[1]
                        else:
                            self.selection_box = pygame.Rect([mx, my, 0, 0])
            elif self.selection_box:
                self.selection_box = None
        
        if 'obj_data_frame' in list(self.widgets.keys()) and self.selected:
            self.widgets['obj_data_frame'].update_data(self.selected)
        
        for obj in self.context.objects:
            if self.context.cam.collide(obj):
                rect = obj.get_rect()
                rect[0] -= self.context.cam.area.x
                rect[1] -= self.context.cam.area.y

                if self.selection_box is not None:
                    selection_box = [
                            self.selection_box.x, 
                            self.selection_box.y,
                            self.selection_box.w,
                            self.selection_box.h
                    ]
                    collision = collide(selection_box, rect)

                    if obj not in self.selection:    
                        if collision:
                            self.selection.append(obj)
                            obj.selected = True
                    elif not collision:
                        self.selection.remove(obj)
                        obj.selected = False
            
        if not self.paused:
            self.context.update(dt)
    
    def draw(self, surface):
        self.context.draw()
        self.surface.blit(self.context.surface, (0, 0))
        
        if self.selection_box:
            pygame.gfxdraw.rectangle(self.surface, self.selection_box, (100, 150, 255, 200))
            pygame.gfxdraw.box(self.surface, self.selection_box, (100, 150, 255, 50))
        
        super().draw(surface)
