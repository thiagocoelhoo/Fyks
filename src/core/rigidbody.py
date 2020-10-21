import numpy as np


class RigidBody:
    def __init__(self, position, velocity, acceleration, mass, charge):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.acceleration = np.array(acceleration, dtype=float)
        self.mass = mass
        self.charge = charge
        self.path = []

        self.offset = np.zeros(2)
        self.forces = []
    
    def add_force(self, x, y):
        force = np.array((x, y))
        self.forces.append(force)
    
    def update(self, dt):
        self.acceleration = np.zeros(2)

        for force in self.forces:
            self.acceleration += force / self.mass

        offset = self.velocity * dt + self.acceleration * dt / 2
        self.velocity += self.acceleration * dt
        self.position += offset
        self.offset += offset
        
        if np.hypot(self.offset[0], self.offset[1]) > 10:
            self.path.insert(0, tuple(self.position))
            self.offset = np.zeros(2)
