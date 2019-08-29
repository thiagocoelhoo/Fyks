import pygame


class EventHandler:
    def __init__(self):
        self.__handlers = {}
    
    def add_handler(self, event, handler):
        if event in self.__handlers:
            self.__handlers[event].append(handler)
        else:
            self.__handlers[event] = [handler]
    
    def update(self):
        for event in pygame.event.get():
            handlers = self.__handlers.get(event.type)
            if handlers:
                for handler in handlers:
                    handler(event)
