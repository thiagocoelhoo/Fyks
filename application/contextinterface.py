import weakref

import pygame

import core
from core import rigidbody
from ui import (
    Frame,
    Layout,
    Button,
    IconButton,
    Label,
    SubWindow,
    Entry,
    OptionsList,
    ItemList
)

mouse = core.get_mouse()


class ObjectDataFrame(Frame):
    def __init__(self, position, obj):
        super().__init__(position, (230, 200))
        self.bg_color = (220, 220, 220)
        self.target = obj
        self.setup_ui()
    
    def setup_ui(self):
        obj = self.target()
        self["position_x_entry"] = Entry("Pos. x", (10, 45), (100, 25), f'{obj.x:.2f}')
        self["position_y_entry"] = Entry("Pos. y", (120, 45), (100, 25), f'{-obj.y:.2f}')
        self["velocity_x_entry"] = Entry("Vel. x", (10, 100), (100, 25), f'{obj.vx:.2f}')
        self["velocity_y_entry"] = Entry("Vel. y", (120, 100), (100, 25), f'{-obj.vy:.2f}')
        self["acceleration_x_entry"] = Entry("Acc. x", (10, 155), (100, 25), f'{obj.ax:.2f}')
        self["acceleration_y_entry"] = Entry("Acc. y", (120, 155), (100, 25), f'{-obj.ay:.2f}')
        # self["mass_entry"] = Entry("Mass", (10, 170), (100, 25), '10.0')
        # self["charge_entry"] = Entry("Charge", (120, 170), (100, 25), '10.0')

    def update(self, dt):
        super().update(dt)
        obj = self.target()
        if obj:
            if not self.widgets['position_x_entry'].active:
                self.widgets['position_x_entry'].text = f'{obj.x:.2f}'
            else:
                try:
                    obj.x = float(self.widgets['position_x_entry'].text)
                except:
                    pass
            
            if not self.widgets['position_y_entry'].active:
                self.widgets['position_y_entry'].text = f'{-obj.y:.2f}'
            else:
                try:
                    obj.y = -float(self.widgets['position_y_entry'].text)
                except:
            
                    pass
            
            if not self.widgets['velocity_x_entry'].active:
                self.widgets['velocity_x_entry'].text = f'{obj.vx:.2f}'
            else:
                try:
                    obj.vx = float(self.widgets['velocity_x_entry'].text)
                except:
                    pass
            
            if not self.widgets['velocity_y_entry'].active:
                self.widgets['velocity_y_entry'].text = f'{-obj.vy:.2f}'
            else:
                try:
                    obj.vy = -float(self.widgets['velocity_y_entry'].text)
                except:
                    pass
            
            if self.widgets['acceleration_x_entry'].active:
                try:
                    f = rigidbody.Force(float(self.widgets['acceleration_x_entry'].text) * obj.mass, 0, None)
                    obj.forces[0] = f
                except:
                    pass
            
            if self.widgets['acceleration_y_entry'].active:
                try:
                    f = rigidbody.Force(0, -float(self.widgets['acceleration_y_entry'].text) * obj.mass, None)
                    obj.forces[1] = f
                except:
                    pass     
        else:
            self.delete()


class ObjectDataFrameList(Layout):
    def add_object(self, obj):
        ref = weakref.ref(obj)
        pos = (0, (len(self.widgets)) * 205)
        self.add(ObjectDataFrame(pos, ref))

    def remove_object(self, obj):
        for widget in self.widgets.copy():
            if obj == widget.target():
                self.widgets.remove(widget)
                break
    
    def clear_list(self):
        self.widgets.clear()


class ContextInterface(Frame):
    def __init__(self, position, size, cframe):
        super().__init__(position, size)
        self.contextframe = cframe
        self.n = 1

        self.eventhandler = core.get_eventhandler()
        self.eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousedown)
    
    # ------------ GUI (Graphic user interface) ----------------

    def setup_ui(self):
        options_frame = Frame((1136, 0), (230, 738))
        context_options = Frame((0, 0), (230, 150))
        context_options['run_time_entry'] = Entry(
            name='Time',
            position=(10, 35),
            size=(160, 25)
        )
        context_options['run_pause_bt'] = Button(
            position=(10, 85),
            size=(100, 25), 
            text='run/pause', 
            func=self.pause
        )

        object_list = ObjectDataFrameList((0, 150))
        options_frame['object_list_frame'] = object_list
        options_frame['context_options_frame'] = context_options

        self.widgets['options_frame'] = options_frame        
        self.widgets['status_label'] = Label('status: None', (20, 20))
        self.widgets['cam_pos_label'] = Label('cam:', (20, 40))
        self.widgets['zoom_label'] = Label("zoom:", (20, 60))
        self.widgets['movement_label'] = Label('movement:', (20, 80))
        
    def show_options(self, mpos):
        options = OptionsList(mpos, (200, 50))
        options.bg_color = core.theme["button-border-color"]
        options.set_options({
            'Add object': self.show_add_object_options,
            # 'Add force': self.show_add_force_options,
            # 'Add forcefield': self.show_add_forcefield_options,
            'Remove': self.contextframe.remove_selected,
            # 'Info': None,
            # 'Exit': None,
        })
        
        self.add_widget('options_menu', options)
    
    def show_edit_object_options(self):
        pass
    
    def show_add_object_options(self):
        # Criar janela de criação de objetos

        frame = SubWindow(mouse.pos, 230, 185, title='Add object')
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

    # ----------------------- ACTIONS --------------------------
    
    def pause(self):
        self.contextframe.toggle_pause()
        try:
            opt_frame = self.widgets['options_frame']
            cxt_opt_frame = opt_frame.widgets['context_options_frame']
            time_entry = cxt_opt_frame.widgets['run_time_entry']
            self.contextframe.endtime = int(time_entry.text or '0')
        except Exception as e:
            print(e)

    def add_object(self, position, mass, charge):
        self.contextframe.add_object(position, mass, charge)
    
    def clear_context(self):
        self.contextframe.clear_context()

    # ----------------------- EVENTS ---------------------------

    def on_mousedown(self, event):
        if self.is_mouse_over():
            if event.button == 1:
                for k in self.widgets:
                    if self.widgets[k].active:
                        self.contextframe.selection_box = None
                        self.active = False
                        break
                else:
                    self.active = True
            elif event.button == 3:
                self.show_options((event.pos[0] - 10, event.pos[1] - 10))

    def update(self, dt):
        super().update(dt)
        self.show_edit_object_options()

        data_frame = self.widgets.get('obj_data_frame')
        if data_frame and self.contextframe.selected:
            data_frame.update_data()
