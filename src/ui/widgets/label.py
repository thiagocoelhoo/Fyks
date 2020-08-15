import pyglet

from ui import Widget


class Label(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lab = pyglet.text.Label(
            font_name='verdana',
            font_size=14,
            color=(61, 85, 94, 255)
        )
    
    @property
    def text(self):
        return self.lab.text
    
    @text.setter
    def text(self, value):
        self.lab.text = value
    
    def draw(self, offset_x=0, offset_y=0):
        self.lab.x = self.x + offset_x
        self.lab.y = self.y + offset_y
        self.lab.draw()
