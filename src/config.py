"""All tunable constants in one place."""

from pathlib import Path

# Window
SCREEN_W = 256
SCREEN_H = 240
TITLE = "platformer"
FPS = 60
ASSETS = str(Path(__file__).resolve().parent.parent / "assets.pyxres")

# World
TILE = 8
TILEMAP = 0
COLLISION_TILES = [
    (1, 0), (2, 0), (2, 1),
    (0, 1), (1, 1), (3, 0),
    (4, 0), (3, 1), (4, 1),
]

# Physics (px per frame at 60 fps)
WALK_SPEED = 1.0
JUMP_SPEED = 3.0       # initial upward speed; fixed arc, no air control
GRAVITY = 0.15
MAX_FALL = 4.0

# Player
PLAYER_W = 10
PLAYER_H = 24
CROUCH_H = 16
SPAWN_X = 16
SPAWN_Y = 70
PLAYER_COLOR = 8
