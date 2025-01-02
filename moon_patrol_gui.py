import lib.g2d as g2d
from moon_patrol_game import MoonPatrolGame
from moon_patrol_game import Background
from config.const import *

class MoonPatrolGui:
    def __init__(self, game: MoonPatrolGame):
        self._game = game
        self._sprite_img = g2d.load_image("res/moon-patrol-sprites.png")
        self._bg_image = g2d.load_image("res/moon_patrol_bg.png")
        self._game_over_img = g2d.load_image("res/game_over.png")
        self._level_complete_img = g2d.load_image("res/level_complete.png")
        self._level = 1
        self._i_heroes = 0
        self._i = 0

    def tick(self):
        self.update_image()
        if self._game.started():
            self.handle_gameplay()
        else:
            self.handle_menu()

    def handle_gameplay(self):
        if not self._game.hero().is_game_over() and (not self._game.is_level_finished() or self._level >= len(BACKGROUNDS_SYMBOLS)):
            self.handle_hero_movement()
            self._game.add_actor()
            self._game.move_all()
        elif self._game.is_level_finished():
            if g2d.key_pressed("Enter"):
                self._level += 1
                self.change_bg_symbol()
                self._game.next_level()
        else:
            if g2d.key_pressed("Enter"):
                self._level = 1
                self._game.restart()

    def handle_hero_movement(self):
        hero = self._game.hero()
        if not hero.is_explode():
            if g2d.key_pressed("ArrowUp"):
                hero.fly_up()
            if g2d.key_pressed("ArrowDown"):
                hero.fly_down()
            if g2d.key_pressed("ArrowLeft"):
                hero.go_left()
            if g2d.key_pressed("ArrowRight"):
                hero.go_right()
            if g2d.key_released("ArrowRight") or g2d.key_released("ArrowLeft"):
                if hero.is_transformed():
                    hero.stay()
                else:
                    hero.go_mid()
            if g2d.key_released("ArrowUp") or g2d.key_released("ArrowDown"):
                hero.stay()
            if g2d.key_pressed("x") or g2d.key_pressed("X"):
                hero.shoot()
            if g2d.key_pressed("Spacebar"):
                hero.go_up()
            if g2d.key_pressed("p") or g2d.key_pressed("P"):
                hero.transform()

    def handle_menu(self):
        if g2d.key_pressed("ArrowRight") and self._i_heroes < len(HEROES_SYMBOLS) - 1:
            self._i_heroes += 1
        if g2d.key_pressed("ArrowLeft") and self._i_heroes > 0:
            self._i_heroes -= 1
        if g2d.key_pressed("Enter"):
            self.change_bg_symbol()
            self.change_hero_csv()
            self._game.start()

    def change_hero_csv(self):
        with open("config/hero_symbol.csv", "w") as f:
            for r in HEROES_SYMBOLS[self._i_heroes]:
                sx, sy, sw, sh = r
                f.write(f"{sx},{sy},{sw},{sh}\n")
        self._game.change_hero()

    def change_bg_symbol(self):
        with open("config/background.csv", "w") as f:
            for r in BACKGROUNDS_SYMBOLS[self._level - 1]:
                sx, sy, sw, sh = r
                f.write(f"{sx},{sy},{sw},{sh}\n")
        self._game.change_bg()

    def draw_score(self):
        ARENA_W, ARENA_H = self._game.arena().size()
        SCORE_RECT = (0, ARENA_H - SCORE_HEIGHT, ARENA_W, SCORE_HEIGHT)

        g2d.set_color((0, 0, 255))
        g2d.fill_rect(SCORE_RECT)
        g2d.set_color((255, 255, 255))
        g2d.draw_text(f"{self._game.get_score()}m", 
                     (BORDER, ARENA_H - SCORE_HEIGHT + BORDER / SCORE_BORDER_OFFSET), 
                     (TEXT_SIZE_W, TEXT_SIZE_H))
        g2d.draw_text(f"Best: {self._game.get_record()}m", 
                     (ARENA_W - BORDER * SCORE_X_OFFSET, ARENA_H - SCORE_HEIGHT + BORDER / SCORE_BORDER_OFFSET), 
                     (TEXT_SIZE_W, TEXT_SIZE_H))
        text = 'reach 400 to advance' if self._level < len(BACKGROUNDS_SYMBOLS) else 'Go for the record'
        g2d.draw_text(text, (ARENA_W / 2 - BORDER * 3, ARENA_H - SCORE_HEIGHT + BORDER / SCORE_BORDER_OFFSET), 
                     (TEXT_SIZE_W, TEXT_SIZE_H))

    def update_image(self):
        ARENA_W, ARENA_H = self._game.arena().size()
        g2d.clear_canvas()
        if self._game.started() and not self._game.hero().is_game_over():
            self.draw_gameplay(ARENA_W, ARENA_H)
        elif self._game.hero().is_game_over():
            self.draw_game_over(ARENA_W, ARENA_H)
        else:
            self.draw_menu(ARENA_W, ARENA_H)

    def draw_gameplay(self, ARENA_W, ARENA_H):
        if not self._game.is_level_finished() or self._level >= len(BACKGROUNDS_SYMBOLS):
            for b in self._game.get_background():
                g2d.draw_image_clip(self._bg_image, b.symbol(), b.position1())
                g2d.draw_image_clip(self._bg_image, b.symbol(), b.position2())
            for a in self._game.arena().actors():
                if not a is self._game.hero():
                    g2d.draw_image_clip(self._sprite_img, a.symbol(), a.position())
            if not self._game.is_game_over():
                g2d.draw_image_clip(self._sprite_img, self._game.hero().symbol(), self._game.hero().position())
            self.draw_score()
        else:
            g2d.draw_image(self._level_complete_img, (0, 0, ARENA_W, ARENA_H))

    def draw_game_over(self, ARENA_W, ARENA_H):
        g2d.draw_image(self._game_over_img, (0, 0, ARENA_W, ARENA_H))
        if self._game.new_best():
            name = g2d.prompt('NUOVO RECORD!!! INSERISCI IL TUO NOME')
            self._game.subscribe_best(name)
        self._level = 1
        self.change_bg_symbol()

    def draw_menu(self, ARENA_W, ARENA_H):
        LOGO_W, LOGO_H = 136, 81
        hx, hy, hw, hh = HEROES_SYMBOLS[self._i_heroes][0]
        g2d.set_color((0, 0, 0))
        g2d.fill_rect((0, 0, ARENA_W, ARENA_H))
        g2d.draw_image_clip(self._sprite_img, 
                          (LOGO_X, LOGO_Y, LOGO_WIDTH, LOGO_HEIGHT),
                          (ARENA_W / 2 - LOGO_WIDTH / 2, ARENA_H / 8, LOGO_WIDTH, LOGO_HEIGHT))
        if self._i >= MENU_BLINK_START:
            if self._i >= MENU_BLINK_END:
                g2d.set_color((0, 0, 0))
                self._i = 0
            else:
                g2d.set_color((0, 255, 0))
        g2d.draw_image_clip(self._sprite_img, (hx, hy, hw, hh), 
                          (ARENA_W / 2 - hw * 1.5, ARENA_H / 2, hw * 2, hh * 3))
        g2d.draw_text('PRESS ENTER TO START', (ARENA_W / 6, MENU_TEXT_Y), (MENU_TEXT_SIZE, MENU_TEXT_SIZE))
        self._i += 1

