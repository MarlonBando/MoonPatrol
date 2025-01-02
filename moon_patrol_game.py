from actors.actor import Actor
from actors.actor import Arena
from actors.hero import Hero
from actors.alien import Alien
from actors.rock import Rock
from actors.hole import Hole
from actors.bonus import Bonus
from config.const import *

import random

class MoonPatrolGame:
    def __init__(self,file:str):
        with open(file,"r") as f1:
            csv = f1.read()
            row = csv.split("\n")
            for r in row:
                element = r.split('=')
                if element[0] == 'ARENA':
                    size = element[1].split(',')
                    self._arena = Arena((int(size[0]),int(size[1])))
                elif element[0] == 'ROVER':
                    size = element[1].split(',')
                    self._hero = Hero(self._arena,(int(size[0]),int(size[1])))
                                         #0.4 velocità primo strato(Montagne)  2.5 velocità secondo strato(colline)
        self._background = [Background(0, 0.4, 0,self._arena), Background(200, 2.5, 1,self._arena), Background(FLOOR,FLOOR_SPEED,2,self._arena)]
        self._delay_spawn = 0
        self._photogram = 0
        self._level = 1
        self._record = 0
        with open("best.txt","r") as f1:
            txt = f1.read()
            best_score = txt.split("=")
            self._record =  int(best_score[1])
        self._level_finished = False
        self._game_start = False
        self._game_over = False
        self._points = 0

    def change_hero(self):
        self._hero.change_symbol()

    def change_bg(self):
        for b in self._background:
            b.change_bg()


    def get_record(self) -> int:
        return self._record
    
    def new_best(self) -> bool:
        if self._record < self._points:
            return True
        else:
            return False

    def subscribe_best(self,name:str):
        with open("best.txt","w") as f1:
            f1.write(name + "=" + str(self._points))
        self._record = self._points
    
    def is_level_finished(self)->bool:
        return self._level_finished

    def next_level(self):
        self._level += 1
        self.restart()
    
    def restart(self):
        for a in self._arena.actors():
            if not isinstance(a,Hero):
                self._arena.remove(a)
        if not self._level_finished:
            self._level = 1
        self._level_finished = False
        self._points = 0
        self._hero.restart()
    
    def add_actor(self):
        rand = random.randrange(201)
        wait = 200      #soglia minima entro il quale deve essere generata o una roccia o una buca
        if rand % 50 == 0 and self._delay_spawn > wait//self._level:
            Hole(FLOOR,512, FLOOR_SPEED,self._arena)
            Bonus(self._arena, self._hero)
            self._delay_spawn = 0
        if rand % (90//self._level) == 0 and self._delay_spawn > wait//self._level:
            # +3 per evitare di veder fluttuare le rocce a causa delle disconnessioni del terreno
            Rock(FLOOR + 3,self._arena) 
            self._delay_spawn = 0
        if rand % (100 // self._level) == 0:
            Alien(self._arena)

    def is_game_over(self):
        return self._game_over
    
    def move_all(self):
        self.game_over = self._hero.is_game_over()
        for b in self._background:
            b.move()
        self._arena.move_all()
        self._photogram += 1
        self._delay_spawn += 1
        self._points += 1
        if self._points >= GOAL:
            self._level_finished = True
            

    def get_score(self) -> int:
        return self._points

    def get_background(self):
        return self._background
    
    def started(self) -> bool:
        return self._game_start
    
    def arena(self) -> Arena:
        return self._arena

    def hero(self) -> Actor:
        return self._hero

    def start(self) -> bool:
        self._game_start = True


class Background:
    def __init__(self,y:int,speed:int,bg_type:int,arena:Arena):
        self._w,self._h = arena.size()
        self._y = y
        self._x1 = 0
        self._x2 = self._w
        self._speed = speed
        self._dx = -speed
        self._bg_type = bg_type #BG type if is 0 means the montains, 1 the climb, 2 floor
        self._backgrounds = []
        self.change_bg()
        if self._bg_type == 0:
            self._h = 280
        else:
            self._h = 127
        self._symbol = self._backgrounds[self._bg_type]

    def move(self):
        if self._x1 < -self._w and self._x2 < 0:
            self._x1 = 0
            self._x2 = self._w
        self._x1 += self._dx
        self._x2 += self._dx

    def change_bg(self):
        self._backgrounds = []
        with open("config/background.csv","r") as f1:
            csv = f1.read()
            row = csv.split("\n")
            for r in row:
                if r != "":
                    s = r.split(",")
                    self._backgrounds.append((int(s[0]),int(s[1]),int(s[2]),int(s[3])))
        self._symbol = self._backgrounds[self._bg_type]
    
    def position1(self):
        return self._x1,self._y,self._w,self._h
    def position2(self):
        return self._x2,self._y,self._w,self._h
    def symbol(self):
        return self._symbol
    def stay(self):
        self._dx = 0

    def restart(self):
        self._dx = -self._speed