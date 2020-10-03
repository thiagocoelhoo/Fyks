import numpy as np
from core.rigidbody import RigidBody


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Context(metaclass=Singleton):
    def __init__(self):
        self._objects = []
        self._frames = []
        self._frame = 0
    
    def _set_frame(self, frame):
        self._frame = frame
        self._frames = self._frames[:frame + 1]
        self._objects.clear()
        for obj in self._frames[frame]:
            rb = RigidBody(obj[0], obj[1], (0, 0), 1, 0)
            self._objects.append(rb)
            for fx, fy in obj[3:]:
                rb.add_force(fx, fy)
        
    def _write_frame(self):
        frame = []
        for obj in self._objects:
            frame.append(
                [
                    np.array((obj.x, obj.y)),
                    obj.velocity,
                    obj.mass,
                    *obj.forces
                ]
            )
        self._frames.append(np.array(frame))
        self._frame += 1

    def _update(self, dt):
        for obj in self._objects:
            obj.update(dt)
        self._write_frame()
