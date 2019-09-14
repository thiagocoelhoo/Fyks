# frame de simulação de particulas (plano cartesiano)
import pygame
import pygame.gfxdraw

from ui import (
    Frame,
    Button,
    Label,
    SubWindow,
    Entry,
    OptionsList,
)
import core
from core.camera import Camera
from core.rigidbody import RigidBody
from core.collisions import collide

mouse = core.get_mouse()


class LinkEntry(Entry):
    def __init__(self, name, position, size, text=''):
        super().__init__(name, position, size, text)
        self.changed = False

    def on_keydown(self, event):
        super().on_keydown(event)
        self.changed = self.active


class ObjectDataFrame(SubWindow):
    def __init__(self, obj):
        super().__init__((20, 40), 300, 340)
        self.color = (100, 100, 100)
        self.autoclear = True

        self['velocity_entry_x'] = Entry("Velocity x", (20, 65), (100, 25))
        self.widgets['velocity_entry_x'].color = (80, 80, 80)
        self['velocity_entry_y'] = Entry("Velocity y", (160, 65), (100, 25))
        self.widgets['velocity_entry_y'].color = (80, 80, 80)

        self['acceleration_entry_x'] = LinkEntry("Acceleration x", (20, 125), (100, 25))
        self.widgets['acceleration_entry_x'].color = (80, 80, 80)
        self['acceleration_entry_y'] = LinkEntry("Acceleration y", (160, 125), (100, 25))
        self.widgets['acceleration_entry_y'].color = (80, 80, 80)
    
        self['force_entry_x'] = LinkEntry("Force x", (20, 185), (100, 25))
        self.widgets['force_entry_x'].color = (80, 80, 80)
        self['force_entry_y'] = LinkEntry("Force y", (160, 185), (100, 25))
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
        
        # ax = self.widgets['acceleration_entry_x'].text
        # ay = self.widgets['acceleration_entry_y'].text

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
        self.mode = 'None'
        self.components = []
        self.selection = []
        self.__selected = None
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
        self.eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousedown)
        self.eventhandler.add_handler(pygame.MOUSEBUTTONUP, self.on_mouseup)
    
    @property
    def selected(self):
        return self.__selected
    
    @selected.setter
    def selected(self, value):
        self.show_object_options(value)
        self.__selected = value
    
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
    
    def show_options(self, mpos):
        options = OptionsList(mpos, (200, 125))
        options.set_options({
            'add': self.show_add_options,
            'remove': None,
            'dinamic': None,
            'info': None,
            'exit': None,
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

    def add_object(self, position, mass):
        if "add_options" in list(self.widgets):
            self.remove_widget("add_options")
        
        obj = RigidBody(position, (0, 0), (0, 0), float(mass))
        self.components.append(obj)
    
    def on_mousedown(self, event):
        if event.button == 3:
            self.show_options((mouse.pos[0] - 10, mouse.pos[1] - 10))
        if event.button == 1 and self.selection:
            self.selected = self.selection[-1]
    
    def on_mouseup(self, event):
        if self.mode != "None":
            self.mode = "None"
    
    def update(self, dt):
        super().update(dt)

        rx, ry = mouse.rel
        mx, my = mouse.pos
        key = pygame.key.get_pressed()

        if self.max_time and self.time >= self.max_time:
            self.paused = True
        
        if key[pygame.K_m]:
            self.mode = "move"
        
        if self.is_mouse_over():
            if mouse.pressed[0]:
                if self.mode == "move":
                    for obj in self.selection:
                        obj.x += rx
                        obj.y += ry
                elif key[pygame.K_LCTRL]:
                    self.cam.area.x -= rx
                    self.cam.area.y -= ry
                else:
                    for k in self.widgets:
                        if self.widgets[k].active:
                            if self.selection_box:
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
        
        for comp in self.components:
            if self.cam.collide(comp):
                comp_rect = (comp.x - self.cam.area.x, comp.y - self.cam.area.y, comp.size[0], comp.size[1])
                if self.selection_box is not None:
                    selection_box = [
                            self.selection_box.x, 
                            self.selection_box.y,
                            self.selection_box.w,
                            self.selection_box.h
                        ]
                    collision = collide(selection_box, comp_rect)

                    if comp not in self.selection:    
                        if collision:
                            self.selection.append(comp)
                            comp.selected = True
                    elif not collision:
                        self.selection.remove(comp)
                        comp.selected = False
            if not self.paused:
                comp.update(dt)
    
    def draw(self, surface):
        self.surface.fill(self.bg_color)
        self.cam.draw_grid(self.surface)
        self.cam.draw_axes(self.surface)
        self.draw_components()
        self.draw_selection_box()
        
        super().draw(surface)
