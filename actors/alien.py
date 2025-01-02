from .actor import Actor
from .actor import Arena
from .bullet import Bullet
from config.const import *
import random

class Alien(Actor):
    def __init__(self, arena: Arena):
        self._w = ALIEN_WIDTH
        self._h = ALIEN_HEIGHT
        self._x = ALIEN_START_X
        self._y = ALIEN_START_Y
        self._movement = ALIEN_MOVEMENTS
        self._dx = random.choice(self._movement)
        self._dy = random.choice(self._movement)
        self._buffer = 0
        arena.add(self)
        self._i = 0
        self._explode = False
        self._explosion = ALIEN_EXPLOSION_FRAMES
        self._arena = arena

    def move(self):
        if not self._explode:
            self._x += self._dx
            self._y += self._dy
            if self._y < ALIEN_BOUNDARY_TOP:
                self._y = ALIEN_BOUNDARY_TOP
            elif self._y > ALIEN_BOUNDARY_BOTTOM:
                self._dy = -self._dy
            if self._x < ALIEN_BOUNDARY_LEFT:
                self._dx = -self._dx
            elif self._x > ALIEN_BOUNDARY_RIGHT:
                self._dx = -self._dx
            if self._buffer >= ALIEN_BUFFER_LIMIT:
                self._dx = random.choice(self._movement)
                self._dy = random.choice(self._movement)
                self._buffer = 0
            self._buffer += 1
            if random.randrange(0, ALIEN_FIRE_CHANCE) == ALIEN_FIRE_THRESHOLD:
                self._arena.add(Bullet(self._arena, (self._x + self._w / 2, self._y + self._h + 5), 0, 4))

        if self._explode and self._i >= len(self._explosion):
            self._arena.remove(self)

    def collide(self, other: Actor):
        if isinstance(other, Bullet):
            b_dx, b_dy = other.direction()
            if b_dy <= 0:
                self._explode = True
                self._w = ALIEN_EXPLOSION_RANGE
                self._h = ALIEN_EXPLOSION_RANGE
        elif not isinstance(other, Alien):
            self._explode = True
            self._w = ALIEN_EXPLOSION_RANGE
            self._h = ALIEN_EXPLOSION_RANGE
    
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        if self._explode and self._i < len(self._explosion):
            x, y, w, h = self._explosion[self._i]
            self._i += 1
            return x, y, w, h
        return ALIEN_SYMBOL