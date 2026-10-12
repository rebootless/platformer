"""Application: window setup and main loop."""

import pyxel

from . import debug, player_view, world
from . import input as controls
from .config import ASSETS, FPS, SCREEN_H, SCREEN_W, TITLE
from .player import Player
from .player_config import SPAWN_X, SPAWN_Y


class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title=TITLE, fps=FPS)
        pyxel.load(ASSETS)
        player_view.load()
        self.player = Player(SPAWN_X, SPAWN_Y)
        pyxel.run(self.update, self.draw)

    def update(self):
        debug.update()
        self.player.update(controls.read())

    def draw(self):
        pyxel.cls(0)
        world.draw()
        player_view.draw(self.player, *debug.preview())
        debug.draw(self.player)
