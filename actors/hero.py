from .actor import Actor
from .bullet import Bullet
from .hole import Hole
from config.const import *


class Hero(Actor):
    def __init__(self, arena, pos):
        self._start_x,self._start_y = pos
        self._x, self._y = self._start_x,self._start_y
        self._w, self._h = HERO_WIDTH, HERO_HEIGHT
        self._speed = HERO_SPEED
        self._dx, self._dy = 0, HERO_INITIAL_DY
        self._arena = arena
        self._game_over = False
        self._explode = False
        self._hit_hole = False
        self._explosion = HERO_EXPLOSION_FRAMES
        self._symbol = []
        self._symbol_bullet = []
        self.change_symbol
        self._buffer = 0
        self._i_explosion = 0
        self._superman = False
        self._time_superman = 0
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        self._buffer += 1
        self._y += self._dy
        self._x += self._dx

        if not self._superman:
            self._dy += HERO_GRAVITY

            if self._y > FLOOR - self._h - 1 and not self._hit_hole:
                self._y = FLOOR - self._h + 1

            if self._x >= HERO_BOUNDARY_RIGHT or self._x <= HERO_BOUNDARY_LEFT or self._x == HERO_CENTER_X:
                self._dx = 0

            if self._y > HERO_FALL_LIMIT - self._h:
                self._dy = 0
                self._explode = True

            if self._explode and self._i_explosion >= len(self._explosion):
                self._game_over = True
        else:
            self._time_superman += 1

            if self._x >= HERO_BOUNDARY_RIGHT:
                self._x = HERO_BOUNDARY_RIGHT - 1

            if self._x <= HERO_BOUNDARY_LEFT:
                self._x = HERO_BOUNDARY_LEFT + 1

            if self._y >= FLOOR - self._h + 1:
                self._y = FLOOR - self._h + 1

            if self._time_superman > HERO_SUPERMAN_DURATION:
                self._time_superman = 0
                self._superman = False
                self._dy = 1

            if self._y <= HERO_BOUNDARY_TOP:
                self._y = HERO_BOUNDARY_TOP

            if self._x <= 0:
                self._x = 0

    def change_symbol(self):
        with open("config/hero_symbol.csv","r") as f1:
            csv = f1.read()
            row = csv.split("\n")
            for i,r in enumerate(row):
                if r != "":
                    s = r.split(",")
                    if i < 3:
                        self._symbol.append((int(s[0]),int(s[1]),int(s[2]),int(s[3])))
                    else:
                        self._symbol_bullet.append((int(s[0]),int(s[1]),int(s[2]),int(s[3])))

     
    def is_game_over(self) -> bool:
        return self._game_over

    def is_explode(self) -> bool:
        return self._explode
    
    def shoot(self):
        bx,by,bw,bh = self.position()
        if self._buffer > HERO_SHOOT_BUFFER:
            Bullet(self._arena, (bx + bw + 1, by + bh / 2), HERO_SHOOT_DX, 0, self)
            self._buffer = 0
        Bullet(self._arena, (bx + bw / 4, by), 0, HERO_SHOOT_DY, self)
    
    def go_left(self):
        self._dx = -self._speed

    def go_right(self):
        self._dx = +self._speed

    def go_mid(self):
        if self._x < HERO_CENTER_X:
            self._dx = self._speed

        if self._x > HERO_CENTER_X:
            self._dx = -self._speed

    def fly_up(self):
        if self._superman:
            self._dy -= self._speed

    def fly_down(self):
        if self._superman:
            self._dy += self._speed

    def go_up(self):
        if self._superman:
            return
    
        if self._explode or self._hit_hole:
            return
        
        if self._y < FLOOR - self._h:
            return
        
        self._dx, self._dy = 0, -self._speed

    def go_down(self):
        self._dx, self._dy = 0, +self._speed

    def stay(self):
        if not self._superman:
            return
        
        self._dx, self._dy = 0, 0

    def collide(self, other):
        if self._superman:
            return
        
        if isinstance(other,Hole) and not self._hit_hole:
            hx,hy,hw,hh = other.position()
            #self._x -= self._x - hx
            self._x -= self._x + self._w - hx
            self._hit_hole = True
            self._dy = 1
        elif not isinstance(other,Hole):
            self._explode = True

    def restart(self):
        self._game_over = False
        self._superman = False
        self._explode = False
        self._hit_hole = False
        self._i_explosion = 0
        self._x, self._y = self._start_x,self._start_y
        self._dx, self._dy = 0, 20
    
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        arena_w, arena_h = self._arena.size()
        if self._explode and self._i_explosion < len(self._explosion):
            x,y,w,h = self._explosion[self._i_explosion]
            self._i_explosion += 1
            return x,y,w,h
        elif self._i_explosion >= len(self._explosion):
            self._game_over = True
        if not self._hit_hole:
            if self._y < arena_h - 90 - self._h:
                return self._symbol[1]
            else:
                return self._symbol[0]
        else:
            return self._symbol[2]
        
    def get_bullet_symbols(self):
        return self._symbol_bullet

    def transform(self):
        self._dy = 0
        self._superman = True

    def is_transformed(self):
        return self._superman