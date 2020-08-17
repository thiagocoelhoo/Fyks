import string

from ui import Entry


class FloatEntry(Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mask = string.digits + '.-'
        self.text = '0.0'
    
    def get_value(self):
        try:
            value = eval(self.text)
        except Exception:
            return 0
        else:
            return value
