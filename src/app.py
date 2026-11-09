import pyxel

from . import debug, hud, player_view, world
from . import input as controls
from .config import ASSETS, FPS, SCREEN_H, SCREEN_W, TITLE, TILEMAP, TILE
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

    def follow(self):
        # Center on the player, clamped to the tilemap bounds.
        tm = pyxel.tilemaps[TILEMAP]
        p = self.player
        x = min(max(p.x + p.w / 2 - SCREEN_W / 2, 0), tm.width * TILE - SCREEN_W)
        y = min(max(p.y + p.h / 2 - SCREEN_H / 2, 0), tm.height * TILE - SCREEN_H)
        pyxel.camera(int(x), int(y))

    def draw(self):
        pyxel.cls(0)
        self.follow()

        world.draw()
        if not debug.monster():
            player_view.draw(self.player, *debug.preview())
        debug.draw(self.player)
        hud.draw(self.player)
