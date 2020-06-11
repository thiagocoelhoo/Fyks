import random
import weakref

import pygame
import pygame.gfxdraw

import core
from core.rigidbody import RigidBody, Force
from core.collisions import collide
from application.context import Context
from application.applicationinterface import ApplicationInterface, ObjectDataFrame

mouse = core.get_mouse()


class ApplicationFrame:
    def __init__(self, master, position, size):
        self.context = Context((size[0] - 200, size[1]))
        self.mode = 'none'
        self.endtime = 0

        self.interface = ApplicationInterface(position, size, self)
        self.interface.autoclear = False
        self.interface.master = master

        self.selection = []
        self.__selected = lambda: None
        self.selection_box = None

        self.eventhandler = core.get_eventhandler()
        self.eventhandler.add_handler(pygame.MOUSEBUTTONDOWN, self.on_mousedown)
        self.eventhandler.add_handler(pygame.MOUSEBUTTONUP, self.on_mouseup)
        self.eventhandler.add_handler(pygame.KEYDOWN, self.on_keydown)
        self.eventhandler.add_handler(pygame.KEYUP, self.on_keyup)
    
    # --------- PROPERTIES ------------

    @property
    def selected(self):
        return self.__selected()
    
    @selected.setter
    def selected(self, value):
        if self.selected:
            self.selected.selected = False
            value.selected = True
        self.interface.show_object_options(value)
        self.__selected = weakref.ref(value)

    # ------- CONTEXT FUNCTIONS ---------
    
    def toggle_pause(self):
        self.context.timer = 0
        self.context.pause()
    
    def show_field(self):
        self.context.show = not self.context.show

    def set_mode(self, mode):
        self.mode = mode
    
    def clear_context(self):
        self.context.clear()

    def add_object(self, position, mass, charge):
        obj = RigidBody((position[0], -position[1]), (0, 0), (0, 0), mass, charge)
        self.context.add_object(obj)
        
        opt_frame = self.interface.widgets['options_frame']
        obj_list = opt_frame.widgets['object_list_frame']
        obj_list.add_object(obj)

    def remove_selected(self):
        opt_frame = self.interface.widgets['options_frame']
        object_list = opt_frame.widgets['object_list_frame']
        
        for obj in self.selection.copy():
            self.selection.remove(obj)
            self.context.remove_object(obj)
            object_list.remove_object(obj)
            obj.delete()
    
    def get_objects(self):
        return self.context.objects
    
    # ----------- EVENTS ---------------
    
    def on_mousedown(self, event):
        if event.button == 1:
            if self.mode == 'none' and self.interface.active:
                if self.selection_box is None:
                    self.selection_box = pygame.Rect([event.pos[0], event.pos[1], 0, 0])
        
        if self.interface.active:
            if event.button == 2:
                self.mode = 'move_spc'
            elif self.context.is_mouse_over():
                if event.button == 4 and self.context.camera.zoom < 10:
                    self.context.camera.cursor = event.pos
                    self.context.camera.zoom += 0.05
                elif event.button == 5 and self.context.camera.zoom > 0.1:
                    self.context.camera.cursor = event.pos
                    self.context.camera.zoom -= 0.05
    
    def on_mouseup(self, event):
        if event.button == 1:
            if self.mode == 'move':
                self.mode = 'none'
            elif self.selection_box is not None:
                self.selection_box = None
        elif event.button == 2:
            self.mode = 'none'
    
    def on_keydown(self, event):
        if event.key == pygame.K_m:
            self.mode = "move"
        elif event.key == pygame.K_SPACE:
            self.toggle_pause()
        elif event.key == pygame.K_DELETE:
            if type(self.selected) == Force:
                self.selected.origin.forces.remove(self.selected)
            else:
                self.remove_selected()
    
    def on_keyup(self, event):
        if event.key == pygame.K_LCTRL:
            self.mode = "none"
    
    # ---------- ESSENCIALS ------------

    def update(self, dt):
        self.interface.update(dt)
        self.context.update(dt)

        if self.context.timer >= self.endtime:
            self.context.paused = True

        rx, ry = mouse.rel
        mx, my = mouse.pos
        
        if self.selection_box is not None:
            self.selection_box.w = mx - self.selection_box[0]
            self.selection_box.h = my - self.selection_box[1]

        if self.interface.is_mouse_over():
            if mouse.pressed[0]:
                if self.mode == "move":
                    for obj in self.selection:
                        obj.x += rx / self.context.camera.zoom
                        obj.y += ry / self.context.camera.zoom
            if self.mode == "move_spc":
                self.context.camera.move(-rx, -ry)
        
        for obj in self.context.objects:
            if self.context.camera.collide(obj):
                if self.selection_box is not None:
                    objx = obj.x*self.context.camera.zoom + self.context.camera.centerx
                    objy = obj.y*self.context.camera.zoom + self.context.camera.centery

                    selection_box = (
                        self.selection_box.x,
                        self.selection_box.y,
                        self.selection_box.w,
                        self.selection_box.h
                    )

                    collision = collide(selection_box, (objx, objy, 20, 20))
                    
                    if obj not in self.selection:    
                        if collision:
                            self.selection.append(obj)
                            obj.selected = True
                    elif not collision:
                        self.selection.remove(obj)
                        obj.selected = False
        
        self.interface.widgets['status_label'].text = f'paused: {self.context.paused}'
        self.interface.widgets['zoom_label'].text = f'zoom: {self.context.camera.zoom}'
        self.interface.widgets['movement_label'].text = f'movement: {self.mode == "move"}'
        
    def draw(self, surface):
        self.context.draw()
        self.interface.surface.blit(self.context.surface, (0, 0))
        
        if self.selection_box:
            pygame.gfxdraw.rectangle(self.interface.surface, self.selection_box, (100, 150, 255, 200))
            pygame.gfxdraw.box(self.interface.surface, self.selection_box, (100, 150, 255, 50))
        
        self.interface.draw(surface)
