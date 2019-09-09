import pygame
import pygame.gfxdraw

from ui import Frame, Button, Label, SubWindow, Entry
import core
from core.camera import Camera
from core.rigidbody import RigidBody

mouse = core.get_mouse()


class ObjectDataFrame(Frame):
    def __init__(self):
        super().__init__((20, 40), (300, 150))
        self.color = (100, 100, 100)
        self.bg_color = (220, 220, 220)

        self['velocity_label'] = Label('velocity:None; None', (20, 20))
        self.widgets['velocity_label'].color = (80, 80, 80)

        self['acceleration_label'] = Label('acceleration:None; None', (20, 50))
        self.widgets['acceleration_label'].color = (80, 80, 80)

        self['position_label'] = Label('position:None; None', (20, 80))
        self.widgets['position_label'].color = (80, 80, 80)

        self['close_bt'] = Button((20, 110), (100, 25), text='close', func=self.close)

    def update_data(self, obj):
        self.widgets['velocity_label'].text = f'velocity:{obj.vx:.2f}; {obj.vy:.2f}'
        self.widgets['acceleration_label'].text = f'acceleration:{obj.ax:.2f}; {obj.ay:.2f}'
        self.widgets['position_label'].text = f'position:{obj.x:.2f}; {obj.y:.2f}'

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
        self.eventhandler.add_handler(pygame.MOUSEMOTION, self.on_mousemotion)
        self.eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousedown)
        self.eventhandler.add_handler(pygame.MOUSEBUTTONUP, self.on_mouseup)
    
    @property
    def selected(self):
        return self.__selected
    
    @selected.setter
    def selected(self, value):
        if not 'obj_data_frame' in list(self.widgets.keys()):
            obj_data_frame = ObjectDataFrame()
            obj_data_frame.master = self
            obj_data_frame.update_data(value)
            self.widgets['obj_data_frame'] = obj_data_frame

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
    
    def draw_overlay(self):
        if self.selected:
            compx = self.selected.x - self.cam.area.x - 20
            compy = self.selected.y - self.cam.area.y - 20
            pygame.gfxdraw.rectangle(self.surface, [compx, compy, 41, 41], (0, 255, 0))

        for comp in self.selection:    
            compx = comp.x - self.cam.area.x - 20
            compy = comp.y - self.cam.area.y - 20
            pygame.gfxdraw.rectangle(self.surface, [compx, compy, 41, 41], (0, 255, 0))
    
    def show_options(self, mpos):
        menu = Frame(mpos, (200, 100))
        menu['add'] = Button((0, 0), (200, 25), 'add', func=self.show_add_options)
        menu['remove'] = Button((0, 25), (200, 25), 'remove', func=self.remove_object)
        menu['view'] = Button((0, 50), (200, 25), 'view')
        menu['exit'] = Button((0, 75), (200, 25), 'exit')
        
        self.widgets['options_menu'] = menu
    
    def show_add_options(self):
        frame = SubWindow(mouse.pos, 230, 135)
        frame.bg_color = (220, 220, 220)
        frame.autoclear = True
        frame["position_x_entry"] = Entry("position x", (10, 60), (100, 25))
        frame["position_y_entry"] = Entry("position y", (120, 60), (100, 25))
        add_func = lambda: self.add_object((int(frame.widgets['position_x_entry'].text), int(frame.widgets['position_y_entry'].text)))
        frame["add_button"] = Button((120, 95), (100, 25), "add", func=add_func)
        self.widgets["add_options"] = frame

    def add_object(self, position):
        if "add_options" in list(self.widgets):
            self.remove_widget("add_options")
        
        obj = RigidBody(position, (0, 0), (0, 0))
        self.components.append(obj)

    def remove_object(self):
        pass

    def hide_options(self):
        try:
            del self.widgets['options_menu']
        except:
            pass
    
    def on_mousemotion(self, event):
        if self.is_inside(event.pos):
            pass
    
    def on_mousedown(self, event):
        if event.button == 3:
            if self.selection:
                self.selected = self.selection[-1]
            else:
                self.show_options((mouse.pos[0] - 5, mouse.pos[1] - 5))

    def on_mouseup(self, event):
        if event.button == 3:
            self.hide_options()

    def update(self, dt):
        super().update(dt)

        rx, ry = mouse.rel
        mx, my = mouse.pos
        key = pygame.key.get_pressed()

        if self.max_time and self.time >= self.max_time:
            self.paused = True
        
        if not self.paused and self.selected and self.selected.vx:
            self.time += dt
            self.x_data.append(self.time)
            self.y_data.append(self.selected.vx)
            w = max(self.x_data) - min(self.x_data) + 1
            h = max(self.y_data) - min(self.y_data) + 1
            y = [i/h*200 for i in self.y_data]
            x = [j/w*200 for j in self.x_data]

            self.widgets['graphic'].plot(x, y)

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

            elif self.selection_box:
                self.selection_box = None
        
        if self.selection and (mouse.pressed[0] or key[pygame.K_LSHIFT]):
            master = self.master
            master.show_comp_menu()
        elif self.widgets.get('comp_view'):
            del self.widgets['comp_view']
        
        if 'obj_data_frame' in list(self.widgets.keys()) and self.selected:
            self.widgets['obj_data_frame'].update_data(self.selected)
        
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
