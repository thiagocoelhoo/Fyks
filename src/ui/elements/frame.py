from .element import Element


class Frame(Element):
    def __init__(self, x, y, w, h, parent=None):
        super().__init__(x, y, w, h, parent)
        self.elements = []
    
    def add(self, element):
        self.elements.append(element)
        element.parent = self
    