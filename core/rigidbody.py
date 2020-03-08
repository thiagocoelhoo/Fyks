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
        # assert n is int
        return Force(self.fx * n, self.fy * n, self.origin)


class RigidBody(Component):
    __instances = []
    __id = 0

    def __init__(self, position, velocity, acceleration, mass, charge):
        super().__init__()
        self.id = self.__id
        self.x, self.y = position
        self.vx, self.vy = velocity
        self.ax, self.ay = acceleration
        self.mass = mass
        self.charge = charge
        self.forces = [Force(0, 0, None), Force(0, 0, None)]
        self.temp_forces = []
        self.r = 20
        self.color = (255, 0, 0)
        self.selected = False
        
        __class__.__instances.append(self)
        __class__.__id += 1

    def delete(self):
        __class__.__instances.remove(self)
    
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
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx += self.ax * dt
        self.vy += self.ay * dt
    
    def update(self, dt):
        self.ax = 0.0
        self.ay = 0.0
        self.temp_forces.clear()

        '''
        # força de campos
        for field in ForceField.get_all():
            dx = (field.x - self.x)
            dy = (field.y - self.y)
            d = (dx**2 + dy**2)**0.5
            f = field.value * self.mass / d**2
            if d < field.size:
                force = Force(dx / d * f, dy / d * f, self)
                self.temp_forces.append(force)
        
        # força elétrica
        for obj in self.__instances:
            if obj != self:
                kqq = 9e9 * self.charge * obj.charge
                dx = (self.x - obj.x)
                dy = (self.y - obj.y)
                d = (dx**2 + dy**2) ** 0.5
                fx = kqq / d**3 * dx
                fy = kqq / d**3 * dy
                force = Force(fx, fy, self)
                self.temp_forces.append(force)
        '''
        
        # aplicação das forças geradas
        for force in self.forces + self.temp_forces:
            self.apply_force(force)
        
        self.update_(dt)
     
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
    __instances = []

    def __init__(self, position, size, value):
        self.x, self.y = position
        self.size = size
        self.value = value
        self.selected = False

        __class__.__instances.append(self)
    
    @classmethod
    def get_all(cls):
        return cls.__instances

    def get_rect(self):
        return [self.x, self.y, 10, 10]

    def update(self, dt):
        pass
