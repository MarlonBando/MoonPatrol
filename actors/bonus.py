from config.const import *
from .actor import Actor
from .bullet import Bullet

class Bonus(Actor):
    def __init__(self, arena, hero):
        self._arena = arena
        arena_w, arena_h = arena.size()
        self._x, self._y = arena_w, arena_h//2
        self._dx = -BONUS_SPEED
        self._w, self._h = BONUS_WIDTH, BONUS_HEIGHT
        self._explode = False
        self._explosion = BONUS_EXPLOSION_FRAMES
        self._i = 0
        self._hero = hero

    def move(self):
        self._x += self._dx

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        if self._explode and self._i < len(self._explosion): #consuma lista contenente symbol dell'esplosione
            x,y,w,h = self._explosion[self._i]
            self._i += 1
            return x,y,w,h

        return BONUS_SYMBOL

    def collide(self, other):
        if not isinstance(other, Bullet):
            return

        b_dx,b_dy = other.direction()
        if b_dx == 0 and b_dy < 0:
            self._explode = True
            self._hero
