import random

import numpy as np


class Component:
    def __init__(self):
        self.selected = False
        self.children = []


class Force(Component):
    def __init__(self, cx, cy, origin):
        super().__init__()
        self.fx = cx
        self.fy = cy
        self.origin = origin
    
    def __mul__(self, n):
        return Force(self.fx * n, self.fy * n, self.origin)


class RigidBody(Component):
    __instances = []
    __id = 0

    def __init__(self, position, velocity, acceleration, mass, charge):
        super().__init__()
        self.id = RigidBody.__id

        self.x, self.y = position
        self.vx, self.vy = velocity
        self.ax, self.ay = acceleration
        self.off_x, self.off_y = 0, 0
        
        self.mass = mass
        self.charge = charge
        self.forces = [Force(0, 0, None), Force(0, 0, None)]
        # self.temp_forces = []
        
        
        self.color = (255, 0, 0)
        self.selected = False
        
        RigidBody.__instances.append(self)
        RigidBody.__id += 1

    def delete(self):
        RigidBody.__instances.remove(self)
    
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

    def update_(self, dt):
        off_x = self.vx * dt + self.ax * dt * dt / 2
        off_y = self.vy * dt + self.ay * dt * dt / 2

        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += off_x
        self.y += off_y
        self.off_x += off_x
        self.off_y += off_y
    
    def update(self, dt):
        self.ax = 0.0
        self.ay = 0.0
        #self.temp_forces.clear()
        
        # aplicação das forças geradas
        
        # for force in self.forces + self.temp_forces:
        for force in self.forces:
            self.apply_force(force)
        
        self.update_(dt)
     
    def draw(self, screen):
        pass
