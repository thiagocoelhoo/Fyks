import pyglet

from app.build import build_main_frame
from app.fileswindow import FileManagerWindow


display = pyglet.canvas.Display()
screen = display.get_default_screen()

WIDTH = screen.width
HEIGHT = screen.height - 25

window = pyglet.window.Window(WIDTH, HEIGHT, "Fyks", resizable=True, vsync=False)
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

frame = build_main_frame(WIDTH, HEIGHT)
window.push_handlers(frame)

fps_label = pyglet.text.Label(
    x=20,
    y=20,
    font_size=14,
    color=(255, 255, 255, 50),
)


@window.event
def on_draw():
    window.clear()
    frame.draw()
    fps_label.draw()


def update(dt):
    frame.update(dt)
    fps_label.text = str(1 / dt)


pyglet.clock.schedule_interval(update, 10e-10)
pyglet.app.run()
