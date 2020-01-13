import random
import weakref

import pygame
import pygame.gfxdraw

import core
from core.camera import Camera
from core.rigidbody import RigidBody, ForceField, Force
from core.collisions import collide
from application.context import Context
from application.contextinterface import ContextInterface, ObjectDataFrame
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
        self.context = Context((size[0] - 200, size[1]))
        self.mode = 'none'
        self.endtime = 0

        self.interface = ContextInterface(position, size, self)
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
            if event.button == 1:
                '''
                if self.mode == 'forcefield-add':
                    ff = ForceField(event.pos, (200, 200), (0.0, 0.0))
                    self.context.add_object(ff)
                    self.mode == 'forcefield-edit'
                elif self.mode == 'measure':
                    if self.mi is not None:
                        self.mode = 'None'
                        self.mi = None
                    else:
                        self.mi = event.pos
                if self.selection:
                    self.selected = self.selection[-1]
                '''
            elif self.context.is_mouse_over() and event.button == 4:
                if self.context.cam.zoom < 10:
                    self.context.cam.zoom += 0.05
            elif self.context.is_mouse_over() and event.button == 5:
                if self.context.cam.zoom > 0.1:
                    self.context.cam.zoom -= 0.05
    
    def on_mouseup(self, event):
        if event.button == 1:
            if self.mode == "move":
                self.mode = "none"
            elif self.selection_box is not None:
                self.selection_box = None
    
    def on_keydown(self, event):
        if event.key == pygame.K_m:
            self.mode = "move"
        elif event.key == pygame.K_LCTRL:
            self.mode = "move_spc"
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
                        obj.x += rx / self.context.cam.zoom
                        obj.y += ry / self.context.cam.zoom
                elif self.mode == "move_spc":
                    self.context.cam.x -= rx / self.context.cam.zoom
                    self.context.cam.y -= ry / self.context.cam.zoom
        
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

        # -----------------update interface labels-------------------

        self.interface.widgets['status_label'].text = f'paused: {self.context.paused}'
        self.interface.widgets['cam_pos_label'].text = f'cam: {self.context.cam.area}'
        self.interface.widgets['zoom_label'].text = f'zoom: {self.context.cam.zoom}'
        self.interface.widgets['movement_label'].text = f'movement: {self.mode == "move"}'
        
    def draw(self, surface):
        self.context.draw()
        self.interface.surface.blit(self.context.surface, (0, 0))

        if self.mode == 'measure' and self.mi is not None:
            pygame.gfxdraw.line(self.interface.surface, *self.mi, *mouse.pos, (50, 200, 150))

        if self.selection_box:
            pygame.gfxdraw.rectangle(self.interface.surface, self.selection_box, (100, 150, 255, 200))
            pygame.gfxdraw.box(self.interface.surface, self.selection_box, (100, 150, 255, 50))
        
        self.interface.draw(surface)
