import random

import numpy as np


class Component:
    def __init__(self):
        self.selected = False
        self.children = []


class Vector:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy


class Force(Component):
    def __init__(self, cx, cy, origin):
        super().__init__()

        self.fx = cx
        self.fy = cy
        self.origin = origin


class RigidBody(Component):
    __instances = []

    def __init__(self, position, velocity, acceleration, mass):
        super().__init__()

        self.x, self.y = position
        self.vx, self.vy = velocity
        self.ax, self.ay = acceleration
        self.mass = mass
        self.forces = []

        self.r = 20
        self.color = (255, 0, 0)
        self.selected = False        

        __class__.__instances.append(self)
    
    @classmethod
    def get_all(cls):
        return cls.__instances

    def get_rect(self):
        return [self.x, self.y, self.r, self.r]
    
    def apply_force(self, force):
        self.ax += force.fx/self.mass
        self.ay += force.fy/self.mass
    
    def add_force(self, force):
        self.forces.append(force)
    
    def remove_force(self, force):
        self.forces.remove(force)

    def update(self, dt):
        for force in self.forces:
            self.apply_force(force)
        
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.ax = 0.0
        self.ay = 0.0
    
    def draw(self, screen):
        '''
        pygame.gfxdraw.circle(screen, int(self.x+width/2), int(height/2 - self.y), 20, (255, 0, 0))
        x1 = int(width/2 + self.x)
        y1 = int(height/2 - self.y)
        x2 = int(width/2 + self.x + self.vx)
        y2 = int(height/2 - (self.y + self.vy))
        pygame.gfxdraw.line(screen, x1, y1, x2, y2, (0, 255, 0))
        '''


class ForceField:
    def __init__(self, position, size, force):
        self.x, self.y = position
        self.w, self.h = size
        self.force = force    
    
    def get_rect(self):
        return [self.x, self.y, self.w, self.h]

    def update(self, dt):
        pass

