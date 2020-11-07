from ui import widgets, elements


class Layout(widgets.Frame, elements.Layout):
    def __init__(self, x, y, w, h, orientation='horizontal', parent=None):
        widgets.Frame.__init__(self, x, y, w, h, parent)
        self.orientation = orientation
    
    def resize(self, width, height):
        super().resize(width, height)
        elements.Layout.resize(self, width, height)