class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls._instances.get(cls) is None:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]