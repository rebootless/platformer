import pyxel

from . import debug


def _text(x, y, s):
    pyxel.text(x + 1, y + 1, s, 0)
    pyxel.text(x, y, s, 7)


def draw(player):
    # HP and debug info, toggled together with F3.
    if not debug.on:
        return
    pyxel.camera()  # screen space: the HUD stays put while the camera moves
    stats = player.stats
    lines = [f"hp {stats.hp}/{stats.max_hp}", *debug.info(player)]
    for i, line in enumerate(lines):
        _text(2, 2 + 8 * i, line)
