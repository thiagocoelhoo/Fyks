class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Context(metaclass=Singleton):
    def __init__(self, x, y, w, h):
        self.w = w
        self.h = h
        self.objects = []

    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)
