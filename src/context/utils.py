import numpy as np
import pyglet

from core.rigidbody import RigidBody


def ctx_add(ctx):
    obj = RigidBody((0, 0), np.random.randint(30, 50, 2), (0, 0), 1, 0)
    obj.forces.append(np.array((0.0, -10.0)))
    ctx.objects.append(obj)


def get_img():
    img = pyglet.image.get_buffer_manager().get_color_buffer()

    contextimg = img.get_region(0, 0, 1100, 700)
    contextimg.save("img.png")
