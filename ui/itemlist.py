from ui import Widget, Label, Button
from render_engine import aa_round_rect


class Item:
    def __init__(self):
        pass


class ItemList(Widget):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.items = [Button((0, 0), (size[0], 25))]

    def draw(self, surface):
        self.surface.fill((0, 0, 0, 0))
        aa_round_rect(
            surface = self.surface, 
            rect = (0, 0, self.w, self.h),
            color = (10, 10, 10),
            rad = 3,
            border = 0,
            inside = (20, 20, 30)
        )
        
        for n, i in enumerate(self.items):
            i.draw(self.surface)
            self.surface.blit(i.surface, (0, n*25))
        
        surface.blit(self.surface, self.pos)
