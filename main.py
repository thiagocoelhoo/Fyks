import os
import numpy as np

import core
core.init()
from application.applicationframe import ApplicationFrame
from application.base import App

width = 1366
height = 738

os.environ['SDL_VIDEO_WINDOW_POS'] = '0, 30'
core.set_theme("aqua-copper")

if __name__ == "__main__":
    app = App(width, height)

    mframe = ApplicationFrame(None, (0, 0), (1366, 738))
    mframe.interface.setup_ui()
    
    app.views['main'] = mframe
    app.current_view = 'main'
    app.run()
