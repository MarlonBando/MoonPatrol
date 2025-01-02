from config.const import *
from .actor import Actor
from .actor import Arena
import random

class Hole(Actor):
    def __init__(self, y: int, x: int, speed: float, arena: Arena):
        self._arena = arena
        self._x = x
        self._y = y
        self._dx = -speed
        self._arena.add(self)
        self._type = random.randrange(0, HOLE_TYPE_COUNT)
        self._w = HOLE_WIDTH
        if self._type % 2 == 0:
            self._h = HOLE_HEIGHT_TYPE_0
        else:
            self._h = HOLE_HEIGHT_TYPE_1
    
    def collide(self, other):
        pass

    def move(self):
        self._x += self._dx
        if self._x < -self._w:
            self._arena.remove(self)

    def position(self) -> (int, int, int, int):
        return self._x, self._y, self._w, self._h

    def symbol(self) -> (int, int, int, int):
        if self._type % 2 == 0:
            return HOLE_SYMBOL_TYPE_0
        else:
            return HOLE_SYMBOL_TYPE_1