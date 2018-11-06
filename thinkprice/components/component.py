from abc import ABC, abstractmethod


class Component:
    def __init__(self, name):
        self.name = name
        self.line = -1
    
    @abstractmethod
    def retrieve(self, schematic):
        pass