import os
import sys

import pyglet
from ui import Frame, Button, Entry, Label


class FileManagerWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(420, 400, 'File manager', vsync=False)
        self.frame = Frame(0, 0, 420, 400)
        self.push_handlers(self.frame)
        self.path = sys.path[0]
        self.build()
    
    def update_dir(self):
        self.files_frame.children.clear()
        for i, directory in enumerate(os.listdir(path=self.path)):
            bt = Button(
                x=0, y=0, 
                w=412, h=30, 
                text=directory,
                command=lambda: self.set_path(directory),
                parent=self.files_frame)
            bt.top = i * 30
            self.files_frame

    def set_path(self, directory):
        self.path = self.path + '\\' + directory
        self.update_dir()
    
    def build(self):
        self.files_frame = Frame(4, 70, 412, 326, parent=self.frame)
        self.update_dir()

        self.entry = Entry(20, 20, 300, 30, parent=self.frame)
        self.save = Button(340, 20, 60, 30, text='save', parent=self.frame)
        
    def on_draw(self):
        self.frame.draw()
