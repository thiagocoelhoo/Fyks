import numpy as np
from core.rigidbody import RigidBody
from utils.singleton import Singleton


class Context(metaclass=Singleton):
    def __init__(self):
        self._objects = []
    
    def _get_objects_data(self):
        for obj in self._objects:
            position = np.array(obj.position, dtype=float)
            velocity = tuple(obj.velocity)
            acceleration = tuple(obj.acceleration)
            forces = np.array(obj.forces, dtype=float)
            yield (position, velocity, acceleration, forces)

    def _set_objects_data(self, data):
        self._objects = []
        for position, velocity, acceleration, forces in data:
            rb = RigidBody(position, velocity, acceleration, 1, 0)
            for force in forces:
                rb.add_force(force[0], force[1])
            self._objects.append(rb)

    def _update(self, dt):
        for obj in self._objects:
            obj.update(dt)
