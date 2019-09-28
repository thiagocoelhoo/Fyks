import weakref

import pygame

import core
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


class ContextInterface(Frame):
    def __init__(self, position, size, cframe):
        super().__init__(position, size)
        self.contextframe = cframe

        self.eventhandler = core.get_eventhandler()
        self.eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousedown)
        self.eventhandler.add_handler(pygame.MOUSEBUTTONUP, self.on_mouseup)
        self.eventhandler.add_handler(pygame.KEYDOWN, self.on_keydown)
        self.eventhandler.add_handler(pygame.KEYUP, self.on_keyup)
    
    # ------------ GUI ----------------

    def show_options(self, mpos):
        options = OptionsList(mpos, (200, 125))
        options.bg_color = core.theme["button-border-color"]
        options.set_options({
            'Add object': self.show_add_object_options,
            'Add force': self.show_add_force_options,
            'Remove': self.contextframe.remove_component,
            'Info': None,
            'Exit': None,
        })
        
        self.add_widget('options_menu', options)
    
    def show_object_options(self, obj):
        if not 'obj_data_frame' in list(self.widgets.keys()):
            obj_data_frame = ObjectDataFrame(obj)
            obj_data_frame.master = self
            obj_data_frame.update_data(obj)
            self.widgets['obj_data_frame'] = obj_data_frame
    
    def show_add_object_options(self):
        frame = SubWindow(mouse.pos, 230, 185)
        frame.autoclear = True

        pos_x_entry = Entry("Position x", (10, 60), (100, 25))
        pos_y_entry = Entry("Position y", (120, 60), (100, 25))
        pos_x_entry.text = "0.00"
        pos_y_entry.text = "0.00"
        mass_entry = Entry("Mass", (10, 115), (100, 25), '10.0')

        frame["position_x_entry"] = pos_x_entry
        frame["position_y_entry"] = pos_y_entry
        frame["mass_entry"] = mass_entry

        def close_func():
            self.widgets["add_options"].delete()
            self.remove_widget("add_options")
        
        def add_func():
            posx = float(frame.widgets['position_x_entry'].text)
            posy = float(frame.widgets['position_y_entry'].text)
            mass = frame.widgets['mass_entry'].text
            self.add_object((posx, posy), mass)
        
        frame["close_button"] = Button((10, 180), (100, 25), "Close", func=close_func)
        frame["add_button"] = Button((120, 180), (100, 25), "Add", func=lambda: add_func() and close_func())
        
        self.widgets["add_options"] = frame

    def show_add_force_options(self):
        frame = SubWindow(mouse.pos, 230, 185)
        frame.autoclear = True

        pos_x_entry = Entry("Force x", (10, 60), (100, 25))
        pos_y_entry = Entry("Force y", (120, 60), (100, 25))
        pos_x_entry.text = "0.00"
        pos_y_entry.text = "0.00"

        frame["force_x_entry"] = pos_x_entry
        frame["force_y_entry"] = pos_y_entry
        
        def close_func():
            self.widgets["add_options"].delete()
            self.remove_widget("add_options")
        
        def add_func():
            fx = float(frame.widgets['force_x_entry'].text)
            fy = float(frame.widgets['force_y_entry'].text)
            self.add_force(fx, -fy)
            close_func()

        frame["close_button"] = Button((10, 180), (100, 25), "Close", func=close_func)
        frame["add_button"] = Button((120, 180), (100, 25), "Add", func=lambda: add_func())
        self.widgets["add_options"] = frame
    
    # ---------- ACTIONS --------------

    def add_object(self, position, mass):
        if "add_options" in list(self.widgets):
            self.remove_widget("add_options")
        self.contextframe.add_object(position, mass)
    
    def add_force(self, fx, fy):        
        force = self.contextframe.add_force(fx, fy)

        if force:
            n = len(self.contextframe.selected.forces) - 1
            self.master.widgets["options_frame"].widgets["vectors_list"].set_options({f"vector {n+1}": force})
    
    # ----------- EVENTS --------------

    def on_mousedown(self, event):
        if self.active:
            if event.button == 3:
                self.show_options((event.pos[0] - 10, event.pos[1] - 10))

    def on_mouseup(self, event):
        pass

    def on_keydown(self, event):
        pass

    def on_keyup(self, event):
        pass
    
    def update(self, dt):
        super().update(dt)

        rx, ry = mouse.rel
        mx, my = mouse.pos

        if self.is_mouse_over():
            if mouse.pressed[0]:
                if self.contextframe.mode == "move":
                    for obj in self.contextframe.selection:
                        obj.x += rx
                        obj.y += ry
                elif self.contextframe.mode == "move_spc":
                    self.contextframe.context.cam.area.x -= rx
                    self.contextframe.context.cam.area.y -= ry
                elif self.contextframe.mode == 'None':
                    for k in self.widgets:
                        if self.widgets[k].active:
                            self.contextframe.selection_box = None
                            self.active = False
                            break
                    else:
                        self.active = True
                        if self.contextframe.selection_box is not None:
                            self.contextframe.selection_box.w = mx - self.contextframe.selection_box[0]
                            self.contextframe.selection_box.h = my - self.contextframe.selection_box[1]
                        else:
                            self.contextframe.selection_box = pygame.Rect([mx, my, 0, 0])
            elif self.contextframe.selection_box:
                self.contextframe.selection_box = None
