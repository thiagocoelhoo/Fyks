#! ./venv/bin/python
import pyglet

from app import interface

display = pyglet.canvas.Display()
screen = display.get_default_screen()

WIDTH = screen.width
HEIGHT = screen.height - 25
FPS = 120
DELTA = 1/FPS


class Application:
    def __init__(self):
        self.window = pyglet.window.Window(
            width=WIDTH, 
            height=HEIGHT, 
            caption="Fyks",
            resizable=True, 
            vsync=False)
        self.window.set_minimum_size(400, 300)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        self.interface = interface.Interface(WIDTH, HEIGHT)
        self.window.push_handlers(self.interface)
        self.window.push_handlers(self)

    def on_draw(self):
        self.window.clear()
        self.interface.draw()

    def update(self, dt):
        self.interface.update(DELTA)

    def run(self):
        pyglet.clock.schedule_interval(self.update, DELTA)
        pyglet.app.run()
