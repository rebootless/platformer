"""Player rendering (placeholder rectangle until a sprite exists)."""

import pyxel

from .config import PLAYER_COLOR


def draw(player):
    pyxel.rect(player.x, player.y, player.w, player.h, PLAYER_COLOR)
