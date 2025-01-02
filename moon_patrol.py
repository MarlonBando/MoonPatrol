import lib.g2d as g2d
from moon_patrol_game import MoonPatrolGame
from moon_patrol_gui  import MoonPatrolGui

game = MoonPatrolGame('config/moon_patrol_game.csv')

g2d.init_canvas(game.arena().size())
ui = MoonPatrolGui(game)
g2d.main_loop(ui.tick)