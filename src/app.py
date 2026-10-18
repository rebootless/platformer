import pyxel

from . import debug, player_view, world
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
        camera_start_pos_temp = 0
        if(self.player.x + SCREEN_W/2 > pyxel.tilemaps[TILEMAP].width * TILE):
            camera_start_pos_temp = pyxel.tilemaps[TILEMAP].width * TILE - SCREEN_W
        elif(self.player.x - SCREEN_W/2 < 0):
            camera_start_pos_temp = 0
        pyxel.camera(camera_start_pos_temp, int(80 - SCREEN_H/2)) # set the camera at a propper limit
        pyxel.run(self.update, self.draw)
        
    def update(self):
        debug.update()
        self.player.update(controls.read())

    def draw(self):
        pyxel.cls(0)
        if self.player.x - SCREEN_W/2 > 0 and self.player.x + SCREEN_W/2 < pyxel.tilemaps[TILEMAP].width * TILE:
            pyxel.camera(int(self.player.x - SCREEN_W/2), int(self.player.y - SCREEN_H/2))
        
        world.draw()
        if not debug.monster():
            player_view.draw(self.player, *debug.preview())
        debug.draw(self.player)
