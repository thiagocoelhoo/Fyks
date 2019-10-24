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
    ItemList
)

mouse = core.get_mouse()


class ObjectDataFrame(SubWindow):
    def __init__(self, obj):
        super().__init__((20, 40), 300, 340, title="RigidBodyConfig")
        self.color = (100, 100, 100)
        self.autoclear = True
        self.target = obj

        self['velocity_entry_x'] = Entry("Velocity x", (20, 65), (100, 25))
        self.widgets['velocity_entry_x'].color = (80, 80, 80)
        self['velocity_entry_y'] = Entry("Velocity y", (160, 65), (100, 25))
        self.widgets['velocity_entry_y'].color = (80, 80, 80)

        self['acceleration_entry_x'] = Entry("Acceleration x", (20, 125), (100, 25))
        self.widgets['acceleration_entry_x'].color = (80, 80, 80)
        self['acceleration_entry_y'] = Entry("Acceleration y", (160, 125), (100, 25))
        self.widgets['acceleration_entry_y'].color = (80, 80, 80)

        '''
        self['force_entry_x'] = Entry("Force x", (20, 185), (100, 25))
        self.widgets['force_entry_x'].color = (80, 80, 80)
        self['force_entry_y'] = Entry("Force y", (160, 185), (100, 25))
        self.widgets['force_entry_y'].color = (80, 80, 80)
        '''

        self['position_entry_x'] = Entry("Position x", (20, 185), (100, 25)) # 20 245
        self.widgets['position_entry_x'].color = (80, 80, 80)
        self['position_entry_y'] = Entry("Position y", (160, 185), (100, 25)) # 160 245
        self.widgets['position_entry_y'].color = (80, 80, 80)

        self['close_bt'] = Button((40, 330), (100, 25), text='close', func=self.close)
        self['apply_bt'] = Button((160, 330), (100, 25), text='apply', func=self.apply)

    def update_data(self):
        '''
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
        '''

        if not self.widgets['velocity_entry_x'].active:
            self.widgets['velocity_entry_x'].text = f'{self.target.vx:.2f}'
        if not self.widgets['velocity_entry_y'].active:
            self.widgets['velocity_entry_y'].text = f'{-self.target.vy:.2f}'

        if not self.widgets['acceleration_entry_x'].active:
            self.widgets['acceleration_entry_x'].text = f'{self.target.ax:.2f}'
        if not self.widgets['acceleration_entry_y'].active:
            self.widgets['acceleration_entry_y'].text = f'{-self.target.ay:.2f}'

        if not self.widgets['position_entry_x'].active:
            self.widgets['position_entry_x'].text = f'{self.target.x:.2f}'
        if not self.widgets['position_entry_y'].active:
            self.widgets['position_entry_y'].text = f'{-self.target.y:.2f}'

    def apply(self):
        vx = self.widgets['velocity_entry_x'].text
        vy = self.widgets['velocity_entry_y'].text

        ax = self.widgets['acceleration_entry_x'].text
        ay = self.widgets['acceleration_entry_y'].text

        px = self.widgets['position_entry_x'].text
        py = self.widgets['position_entry_y'].text
        
        try:
            self.target.vx = float(vx)
            self.target.vy = -float(vy)
            self.target.ax = float(ax)
            self.target.ay = -float(ay)
            self.target.x = float(px)
            self.target.y = -float(py)

            self.bg_color = core.theme['frame-background-color']
        except:
            self.bg_color = (230, 210, 210)

    def close(self):
        self.master.remove_widget('obj_data_frame')


class ContextInterface(Frame):
    def __init__(self, position, size, cframe):
        super().__init__(position, size)
        self.contextframe = cframe
        self.n = 1

        self.eventhandler = core.get_eventhandler()
        self.eventhandler.add_handler(pygame.VIDEORESIZE, self.on_resize)
        self.eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousedown)
        self.eventhandler.add_handler(pygame.MOUSEBUTTONUP, self.on_mouseup)
        self.eventhandler.add_handler(pygame.KEYDOWN, self.on_keydown)
        self.eventhandler.add_handler(pygame.KEYUP, self.on_keyup)
    
    # ------------ GUI (Graphic user interface) ----------------

    def setup_ui(self):
        options_frame = Frame((1166, 0), (200, 738))

        options_frame['run_time_entry'] = Entry('Time', (20, 35), (160, 25))
        options_frame['run_pause_bt'] = Button((20, 85), (100, 25), text='run/pause', func=self.pause)
        options_frame['mode_bt'] = Button((20, 135), (100, 25), text='interagente', func=self.contextframe.set_intg)
        options_frame['clear_bt'] = Button((20, 185), (100, 25), text='clear', func=self.contextframe.clear_context)
        options_frame['show_mesh'] = Button((20, 235), (100, 25), text='show field', func=self.contextframe.show_field)

        # vector_list = OptionsList((20, 235), (160, 300))
        vector_list = ItemList((20, 285), (160, 300))
        vector_list.close_after = False
        vector_list.bg_color = (150, 150, 180)
        options_frame['vectors_list'] = vector_list
        
        self.widgets['options_frame'] = options_frame
        self.widgets['status_label'] = Label('status: None', (20, 20))
        self.widgets['cam_pos_label'] = Label('cam:', (20, 40))
        self.widgets['zoom_label'] = Label("zoom:", (20, 60))
        self.widgets['movement_label'] = Label('movement:', (20, 80))

    def clear_context(self):
        self.contextframe.clear_context()
    
    def show_options(self, mpos):
        options = OptionsList(mpos, (200, 125))
        options.bg_color = core.theme["button-border-color"]
        options.set_options({
            'Add object': self.show_add_object_options,
            'Add force': self.show_add_force_options,
            'Add forcefield': self.show_add_forcefield_options,
            'Remove': self.contextframe.remove_component,
            'Info': None,
            'Exit': None,
        })
        
        self.add_widget('options_menu', options)

    def show_object_options(self, obj):
        if type(obj) == core.rigidbody.RigidBody and not 'obj_data_frame' in list(self.widgets.keys()):
            obj_data_frame = ObjectDataFrame(obj)
            obj_data_frame.master = self
            obj_data_frame.update_data()
            self.widgets['obj_data_frame'] = obj_data_frame

    def show_add_object_options(self):
        # Criar janela de criação de objetos

        frame = SubWindow(mouse.pos, 230, 185)
        frame.autoclear = True

        frame["position_x_entry"] = Entry("Position x", (10, 60), (100, 25), '0.00')
        frame["position_y_entry"] = Entry("Position y", (120, 60), (100, 25), '0.00')
        frame["mass_entry"] = Entry("Mass", (10, 115), (100, 25), '10.0')
        frame["charge_entry"] = Entry("Charge", (120, 115), (100, 25), '10.0')

        def close_func():
            self.widgets["add_options"].delete()
            self.remove_widget("add_options")
        
        def add_func():
            posx = float(frame.widgets['position_x_entry'].text)
            posy = float(frame.widgets['position_y_entry'].text)
            mass = float(frame.widgets['mass_entry'].text)
            charge = float(frame.widgets['charge_entry'].text)
        
            self.add_object((posx, posy), mass, charge)
            close_func()
        
        frame["close_button"] = Button((10, 180), (100, 25), "Close", func=close_func)
        frame["add_button"] = Button((120, 180), (100, 25), "Add", func=add_func)
        
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

    def show_add_forcefield_options(self):
        # Criar janela de criação de campos de força

        frame = SubWindow(mouse.pos, 230, 185)
        frame.autoclear = True

        frame["position_x_entry"] = Entry("Position X", (10, 60), (100, 25), '0.00')
        frame["position_y_entry"] = Entry("Position Y", (120, 60), (100, 25), '0.00')
        frame["force_entry"] = Entry("Force (Newtons)", (10, 115), (100, 25), '10.0')

        def close_func():
            self.widgets["add_options"].delete()
            self.remove_widget("add_options")
        
        def add_func():
            posx = float(frame.widgets['position_x_entry'].text)
            posy = float(frame.widgets['position_y_entry'].text)
            force = frame.widgets['force_entry'].text
        
            self.add_forcefield((posx, posy), force)
            close_func()
        
        frame["close_button"] = Button((10, 180), (100, 25), "Close", func=close_func)
        frame["add_button"] = Button((120, 180), (100, 25), "Add", func=add_func)
        
        self.widgets["add_options"] = frame

    # ----------------------- ACTIONS --------------------------

    def pause(self):
        self.contextframe.toggle_pause()
    
        try:
            self.contextframe.max_time = int(self.widgets['options_frame'].widgets['run_time_entry'].text or '0')
        except Exception as e:
            print(e)

        self.widgets['status_label'].text = f'paused: {self.contextframe.paused}'

    def add_object(self, position, mass, charge):
        self.contextframe.add_object(position, mass, charge)

    def add_force(self, fx, fy):
        force = self.contextframe.add_force(fx, fy)
        
        if force:
            # n = len(self.contextframe.selected.forces) - 1
            # self.master.widgets["options_frame"].widgets["vectors_list"].set_options({f"vector {self.n}": force})
            m = self.widgets["options_frame"].widgets["vectors_list"]
            m[f"vec {self.n}"] = force
            self.n += 1

    def add_forcefield(self, position, force):
        self.contextframe.add_forcefield(position, force)

    # ----------------------- EVENTS ---------------------------

    def on_resize(self, event):
        print(event)
        print(pygame.display.get_surface())

    def on_mousedown(self, event):
        if self.is_mouse_over():
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
                        obj.x += rx / self.contextframe.context.cam.zoom
                        obj.y += ry / self.contextframe.context.cam.zoom
                elif self.contextframe.mode == "move_spc":
                    self.contextframe.context.cam.x -= rx / self.contextframe.context.cam.zoom
                    self.contextframe.context.cam.y -= ry / self.contextframe.context.cam.zoom
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

        self.widgets['status_label'].text = f'paused: {self.contextframe.paused}'
        self.widgets['cam_pos_label'].text = f'cam: {self.contextframe.context.cam.area}'
        self.widgets['zoom_label'].text = f'zoom: {self.contextframe.context.cam.zoom}'
        self.widgets['movement_label'].text = f'movement: {self.contextframe.mode == "move"}'

        data_frame = self.widgets.get('obj_data_frame')
        if data_frame and self.contextframe.selected:
            data_frame.update_data()
