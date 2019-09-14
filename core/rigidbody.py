class RigidBody:
    __instances = []

    def __init__(self, position, velocity, acceleration, mass):
        RigidBody.__instances.append(self)
        self.x, self.y = position
        self.vx, self.vy = velocity
        self.ax, self.ay = acceleration
        self.mass = mass
        self.r = 20
        self.color = (255, 0, 0)
        self.selected = False
    
    def get_rect(self):
        return [self.x, self.y, self.r, self.r]
    
    def apply_force(self, force):
        self.ax = force[0]/self.mass
        self.ay = force[1]/self.mass
    
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx += self.ax * dt
        self.vy += self.ay * dt
    
    def draw(self, screen):
        '''
        pygame.gfxdraw.circle(screen, int(self.x+width/2), int(height/2 - self.y), 20, (255, 0, 0))
        x1 = int(width/2 + self.x)
        y1 = int(height/2 - self.y)
        x2 = int(width/2 + self.x + self.vx)
        y2 = int(height/2 - (self.y + self.vy))
        pygame.gfxdraw.line(screen, x1, y1, x2, y2, (0, 255, 0))
        '''
    
    @classmethod
    def get_all(cls):
        return cls.__instances


class ForceField:
    def __init__(self, position, size, force):
        self.x, self.y = position
        self.w, self.h = size
        self.force = force    
    
    def get_rect(self):
        return [self.x, self.y, self.w, self.h]

    def update(self, dt):
        pass
