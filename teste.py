import time


def measure(func):
    def meassure_func(*args, **kwargs):
        a = time.time()
        r = func(*args, **kwargs)
        b = time.time()

        print('time:', b - a)

        return r
    return meassure_func


@measure
def contar(a, b):
    for i in range(a, b+1):
        print(i)


# contar(0, 10)

@measure
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def say_hello(self):
        print(f'Hello, my name is {self.name}, i\'m {self.age} years old')


ana = Person('Ana', 17)
ana.say_hello()
