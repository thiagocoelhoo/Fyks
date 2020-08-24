import os
import sys

import pyglet
from ui import Frame, Button, Entry, Label


def command(func):
    def wrapper(*args, **kwargs):
        return lambda: func(*args, **kwargs)
    return wrapper


class FileManagerWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(650, 370, 'File manager', vsync=False)
        self.frame = Frame(0, 0, 650, 370)
        self.path = sys.path[0]
        self.build()
        self.push_handlers(self.frame)
    
    def update_path(self):
        self.path_entry.text = self.path
        self.directory_frame.children.clear()
        for n, directory in enumerate(os.listdir(path=self.path)):
            bt = Button(
                x=5, y=0, 
                w=550, h=25, 
                text=directory,
                command=self.open_folder_command(directory),
                parent=self.directory_frame)
            bt.border_radius = 5
            bt.top = n * 30 + 5
    
    def open_folder(self, directory):
        self.path = f'{self.path}\\{directory}'
        self.update_path()
    
    open_folder_command = command(open_folder)
    
    def to_back(self):
        path = self.path.split('\\')
        self.path = '\\'.join(path[:-1])
        self.update_path()

    def build(self):
        self.back_bt = Button(
            x=5, y=0, w=76, h=26,
            text='Voltar',
            command=self.to_back,
            parent=self.frame)
        self.back_bt.top = 5

        self.path_entry = Entry(
            x=85, y=0, w=560, h=25,
            parent=self.frame)
        self.path_entry.top = 5

        self.directory_frame = Frame(x=85, y=0, w=560, h=290, parent=self.frame)
        self.directory_frame.top = 35
        self.directory_frame.border_radius = 5
        self.update_path()

        self.entry = Entry(x=5, y=8, w=555, h=30, parent=self.frame)
        self.entry.text = 'untitled'

        self.save = Button(
            x=565, y=8,
            w=80, h=30,
            text='Confirmar',
            command=self.submit,
            parent=self.frame)
    
    def submit(self):
        pass

    def on_draw(self):
        self.frame.draw()
