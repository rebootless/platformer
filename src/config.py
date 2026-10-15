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
