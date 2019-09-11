import weakref

import pygame


class EventHandler:
    def __init__(self):
        self.__handlers = {}
    
    def add_handler(self, event, handler):
        ref = weakref.WeakMethod(handler)
        if event in self.__handlers:
            self.__handlers[event].append(ref)
        else:
            self.__handlers[event] = [ref]
    
    def update(self):
        for event in pygame.event.get():
            handlers = self.__handlers.get(event.type)
            if handlers:
                for handler in handlers:
                    f = handler()
                    if f:
                        f(event)
