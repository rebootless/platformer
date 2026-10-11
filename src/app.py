"""Application: window setup and main loop."""

import pyxel

from . import input as controls
from . import player_view, world
from .config import ASSETS, FPS, SCREEN_H, SCREEN_W, SPAWN_X, SPAWN_Y, TITLE
from .player import Player


class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title=TITLE, fps=FPS)
        pyxel.load(ASSETS)
        self.player = Player(SPAWN_X, SPAWN_Y)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update(controls.read())

    def draw(self):
        pyxel.cls(0)
        world.draw()
        player_view.draw(self.player)
