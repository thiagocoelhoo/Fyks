import core
core.init()
from application.application import App
from ui import Frame

WIDTH = 800
HEIGHT = 600

if __name__ == "__main__":
    app = App(WIDTH, HEIGHT)
    app.views["main"] = Frame((0, 0), (WIDTH, HEIGHT))
    app.views["main"].bg_color = (220, 220, 220)
    app.current_view = "main"
    app.run()
