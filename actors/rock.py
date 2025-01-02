from config.const import *
from .actor import Actor
from .actor import Arena
from .hole import Hole
from .hero import Hero
import random

class Rock(Actor):
    def __init__(self,y:int,arena:Arena):
        arena_w,arena_h = arena.size()
        self._x = arena_w
        self._type = random.randrange(0,2)
        if self._type % 2 == 0:
            self._symbol = ROCK_SMALL_SYMBOL
            self._w = ROCK_SMALL_WIDTH
            self._h = ROCK_SMALL_HEIGHT
            self._life = ROCK_SMALL_LIFE
        else:
            self._symbol = ROCK_LARGE_SYMBOL
            self._w = ROCK_LARGE_WIDTH
            self._h = ROCK_LARGE_HEIGHT
            self._life = ROCK_LARGE_LIFE
        self._y = y - self._h
        self._dx = FLOOR_SPEED
        self._explosion = ROCK_EXPLOSION_FRAMES
        self._i_explosion = 0
        self._explode = False
        arena.add(self)
        self._arena = arena

    def move(self):
        self._x -= self._dx
        if self._x < -self._w:
            self._arena.remove(self)
        if self._explode and self._i_explosion >= len(self._explosion):
            self._arena.remove(self)
            
    def collide(self,other):
        if isinstance(other,Hole):
            self._x += ROCK_HOLE_OFFSET
        elif not isinstance(other,Hero): 
            self._life -= 1
            if self._life <= 0:
                self._explode = True
        
        
    def position(self):
        return self._x,self._y,self._w,self._h

    def symbol(self):
        if self._explode and self._i_explosion < len(self._explosion):
            x,y,w,h = self._explosion[self._i_explosion]
            self._i_explosion += 1
            return x,y,w,h
        
        return self._symbol