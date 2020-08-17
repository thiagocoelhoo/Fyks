import numpy as np
import pyglet

from core.rigidbody import RigidBody


def get_img(size):
    img = pyglet.image.get_buffer_manager().get_color_buffer()

    contextimg = img.get_region(0, 0, 1100, 700)
    contextimg.save("img.png")
