import pyglet
from pyglet.gl import *
from pyglet.graphics import *


class Widget:
    def __init__(self, position, size):
        self.x, self.y = position
        self.w, self.h = size


class Container(Widget):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.widgets = {}


class Window(pyglet.window.Window):
    def __init__(self, width, height, title=''):
        super().__init__(width, height, title)
        pyglet.gl.glClearColor(1, 1, 1, 1)
        pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
        self.main_container = Container((0, 0), (width, height))
    
    def on_draw(self):
        self.clear()


w = Window(400, 400)
pyglet.app.run()
