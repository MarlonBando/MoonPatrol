from .actor import Actor
from .actor import Arena
from .hole import Hole
from .alien import Alien
from .hero import Hero
from config.const import *

import random

class Bullet(Actor):
    def __init__(self, arena:Arena,pos:(int,int),dx:int,dy:int,hero=None):
        self._x, self._y = pos
        self._w, self._h = BULLET_WIDTH, BULLET_HEIGHT
        self._dy, self._dx = dy, dx
        arena.add(self)
        if self._dx > 0 or dy < 0:
            self._explosion = BULLET_EXPLOSION_FRAMES_1
        else:
            self._explosion = BULLET_EXPLOSION_FRAMES_2
        if hero != None:
            self._bullet_symbol = hero.get_bullet_symbols()
        self._arena = arena
        self._i_explosion = 0
        self._explode = False
        self._movement = 0

    def move(self): 
        if self._explode:
            self._handle_explosion()
        else:
            self._update_position()
            self._check_collisions()
            self._movement += 1

    def _update_position(self):
        self._x += self._dx
        self._y += self._dy

    def _check_collisions(self):
        if self._movement >= BULLET_HORIZONTAL_MAX_DISTANCE and self._dx > 0:
            self.collide(self)
        if self._y + self._h < 0 or self._y >= FLOOR + 1:
            self.collide(self)

    def _handle_explosion(self):
        if self._i_explosion >= len(self._explosion):
            self._maybe_spawn_hole()
            self._arena.remove(self)

    def _maybe_spawn_hole(self):
        if self._dy > 0 and self._y >= BULLET_GROUND_Y_THRESHOLD and random.randrange(BULLET_HOLE_SPAWN_CHANCE) == BULLET_HOLE_SPAWN_THRESHOLD:
            self._arena.add(Hole(FLOOR, self._x - BULLET_HOLE_X_OFFSET, FLOOR_SPEED, self._arena))

    def collide(self, other):
        if isinstance(other, (Hero, Alien)):
            self._arena.remove(self)
            return

        if isinstance(other, Bullet) and self._is_same_direction(other):
            return

        self._trigger_explosion()

    def _is_same_direction(self, other):
        return self.direction() == other.direction() == (0, -10)

    def _trigger_explosion(self):
        self._explode = True
        if self._dy > 0:
            self._set_ground_explosion_dimensions()
        else:
            self._set_air_explosion_dimensions()

    def _set_ground_explosion_dimensions(self):
        self._w = BULLET_GROUND_EXPLOSION_WIDTH
        self._h = BULLET_GROUND_EXPLOSION_HEIGHT
        self._y -= self._h - BULLET_GROUND_EXPLOSION_Y_OFFSET

    def _set_air_explosion_dimensions(self):
        self._w = BULLET_AIR_EXPLOSION_SIZE
        self._h = BULLET_AIR_EXPLOSION_SIZE

    def direction(self)->(int,int):
        return self._dx,self._dy
            
    def isExploded(self):
        return self._explode

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        if self._dx > 0 and self._dy == 0 and not self._explode:
            return self._bullet_symbol[0]
        elif self._dy < 0 and self._dx == 0 and not self._explode:
            return self._bullet_symbol[1]
        elif self._dy > 0 and self._dx == 0 and not self._explode:
            return 213,231,5,6
        
        if self._explode and self._i_explosion < len(self._explosion):
            x,y,w,h = self._explosion[self._i_explosion]
            self._i_explosion += 1
            return x,y,w,h

        return 0,0,0,0