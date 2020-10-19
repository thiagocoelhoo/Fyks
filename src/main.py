import pyglet

from app.build import build_main_frame

display = pyglet.canvas.Display()
screen = display.get_default_screen()

WIDTH = screen.width
HEIGHT = screen.height - 25
FPS = 200
DELTA = 1/FPS

window = pyglet.window.Window(WIDTH, HEIGHT, "Fyks", resizable=True, vsync=False)
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

frame = build_main_frame(WIDTH, HEIGHT)
window.push_handlers(frame)


@window.event
def on_draw():
    window.clear()
    frame.draw()

def update(dt):
    frame.update(DELTA)


pyglet.clock.schedule_interval(update, DELTA)
pyglet.app.run()
