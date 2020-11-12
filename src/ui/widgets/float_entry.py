import string

from ui import widgets


class FloatEntry(widgets.Entry):
    def __init__(self, x, y, w, h, parent=None):
        super().__init__(x, y, w, h, parent)
        self.mask = string.digits + '.-'
        self.text = '0.0'
    
    def get_value(self):
        try:
            value = eval(self.text)
        except Exception:
            return 0
        else:
            return value
