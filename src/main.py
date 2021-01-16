#! ./venv/bin/python
import pyglet

from app.interface import Interface

display = pyglet.canvas.Display()
screen = display.get_default_screen()

WIDTH = screen.width
HEIGHT = screen.height - 25
FPS = 120
DELTA = 1/FPS


def main():    
    window = pyglet.window.Window(
        width=WIDTH, 
        height=HEIGHT, 
        caption="Fyks",
        resizable=True, 
        vsync=False)
    window.set_minimum_size(400, 300)
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    interface = Interface(WIDTH, HEIGHT)
    window.push_handlers(interface)

    @window.event
    def on_draw():
        window.clear()
        interface.draw()

    def update(dt):
        interface.update(DELTA)

    pyglet.clock.schedule_interval(update, DELTA)
    pyglet.app.run()
