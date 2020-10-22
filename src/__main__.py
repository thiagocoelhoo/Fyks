#! ./venv/bin/python
import pyglet

from app.init import init_ui

display = pyglet.canvas.Display()
screen = display.get_default_screen()

WIDTH = screen.width
HEIGHT = screen.height - 25
FPS = 120
DELTA = 1/FPS


def main():
    try:
        config = pyglet.gl.Config(
            sample_buffers=1, 
            samples=4,
            depth_size=16,
            double_buffer=True)
        window = pyglet.window.Window(
            width=WIDTH, 
            height=HEIGHT, 
            caption="Fyks", 
            config=config,
            resizable=True, 
            vsync=False)
    except pyglet.window.NoSuchConfigException:
        print('Error: noSuchConfigException')
        window = pyglet.window.Window(
            width=WIDTH, 
            height=HEIGHT, 
            caption="Fyks",
            resizable=True, 
            vsync=False)
    
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    frame = init_ui(WIDTH, HEIGHT)
    window.push_handlers(frame)


    @window.event
    def on_draw():
        window.clear()
        frame.draw()


    def update(dt):
        frame.update(DELTA)


    pyglet.clock.schedule_interval(update, DELTA)
    pyglet.app.run()


if __name__ == '__main__':
    main()
