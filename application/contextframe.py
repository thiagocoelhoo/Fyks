import random
import weakref

import pygame
import pygame.gfxdraw

import core
from core.camera import Camera
from core.rigidbody import RigidBody, ForceField, Force
from core.collisions import collide
from application.context import Context
from application.contextinterface import ContextInterface
from ui import (
    Frame,
    Button,
    Label,
    SubWindow,
    Entry,
    OptionsList,
)

mouse = core.get_mouse()


class ContextFrame:
    def __init__(self, master, position, size):
        self.context = Context(size)
        self.interface = ContextInterface(position, size, self)
        self.interface.autoclear = False
        self.interface.master = master

        self.mode = 'None'
        self.paused = True
        self.max_time = 0

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
    
    @property
    def widgets(self):
        return self.interface.widgets

    # ------- CONTEXT FUNCTIONS ---------

    def toggle_pause(self):
        self.paused = not self.paused

    def add_object(self, position, mass):
        obj = RigidBody((position[0], -position[1]), (0, 0), (0, 0), float(mass))
        self.context.add_object(obj) 

    def add_force(self, fx, fy):
        if self.selected:
            force = Force(fx, fy, self.selected)
            self.selected.add_force(force)

            def f():
                self.selected = force
            
            return f

    def remove_component(self):
        if self.selected:
            self.context.remove(self.selected)
    
    # ----------- EVENTS ---------------
    
    def on_mousedown(self, event):
        if self.interface.active:
            if event.button == 1:
                if self.mode == 'forcefield-add':
                    ff = ForceField(event.pos, (200, 200), (0.0, 0.0))
                    self.context.add_object(ff)
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
        elif event.key == pygame.K_DELETE:
            if type(self.selected) == Force:
                self.selected.origin.forces.remove(self.selected)
    
    def on_keyup(self, event):
        if event.key == pygame.K_LCTRL:
            self.mode = "None"
    
    # ---------- ESSENCIALS ------------

    def update(self, dt):
        self.interface.update(dt)

        rx, ry = mouse.rel
        mx, my = mouse.pos

        if self.max_time and self.context.time >= self.max_time:
            self.paused = True
        
        if 'obj_data_frame' in list(self.interface.widgets.keys()) and type(self.selected) == RigidBody:
            self.interface.widgets['obj_data_frame'].update_data(self.selected)
        
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
        self.interface.surface.blit(self.context.surface, (0, 0))
        
        if self.selection_box:
            pygame.gfxdraw.rectangle(self.interface.surface, self.selection_box, (100, 150, 255, 200))
            pygame.gfxdraw.box(self.interface.surface, self.selection_box, (100, 150, 255, 50))
        
        self.interface.draw(surface)
