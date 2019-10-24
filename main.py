import os
import numpy as np

import core
core.init()
from application.contextframe import ContextFrame
from application.base import App

width = 1366
height = 738


os.environ['SDL_VIDEO_WINDOW_POS'] = f'0, 30'
core.set_theme("aqua-copper")

if __name__ == "__main__":
    app = App(width, height)
    mframe = ContextFrame(None, (0, 0), (1366, 738))
    for i in range(10):
        mframe.add_object(np.random.randint(-100, 100, 2), np.random.random(), np.random.uniform(-0.001, 0.001))
    mframe.interface.setup_ui()
    app.views['main'] = mframe
    app.current_view = 'main'
    app.run()
