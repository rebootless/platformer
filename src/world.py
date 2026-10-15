import pyxel

from .config import COLLISION_TILES, SCREEN_H, SCREEN_W, TILE, TILEMAP


def solid(px, py):
    # True if the pixel position is inside a collision tile.
    if px < 0 or px >= SCREEN_W:
        return True  # screen edges act as walls
    if py < 0:
        return False
    return pyxel.tilemaps[TILEMAP].pget(px // TILE, py // TILE) in COLLISION_TILES


def box_hits(x, y, w, h):
    # True if the box overlaps any solid tile.
    return any(
        solid(px, py)
        for px in (int(x), int(x + w - 1))
        for py in (int(y), int(y + h // 2), int(y + h - 1))
    )


def draw():
    pyxel.bltm(0, 0, TILEMAP, 0, 0, SCREEN_W, SCREEN_H, 0)
