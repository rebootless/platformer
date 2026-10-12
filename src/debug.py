"""F3 debug overlay: hitbox, sprite cell, player info and an animation previewer.

F3 toggles the overlay. While it is on, [ and ] step through every animation
(including the ones the game does not use yet); the first slot is the live one.
"""

import pyxel

from . import player_view
from .anims import ANIMS, SPRITE_H, SPRITE_W

on = False
_names = list(ANIMS)
_slot = 0       # 0 = live animation, 1.. = _names[slot - 1] looped
_tick = 0


def update():
    global on, _slot, _tick
    if pyxel.btnp(pyxel.KEY_F3):
        on = not on
        _slot = 0
    if not on:
        return
    step = pyxel.btnp(pyxel.KEY_RIGHTBRACKET) - pyxel.btnp(pyxel.KEY_LEFTBRACKET)
    if step:
        _slot = (_slot + step) % (len(_names) + 1)
        _tick = 0
    else:
        _tick += 1


def preview():
    """(state, tick) to draw instead of the live animation, or (None, 0)."""
    if not on or _slot == 0:
        return None, 0
    name = _names[_slot - 1]
    frames, ticks, _ = ANIMS[name]
    return name, _tick % (frames * ticks)


def _text(x, y, s):
    pyxel.text(x + 1, y + 1, s, 0)
    pyxel.text(x, y, s, 7)


def draw(player):
    if not on:
        return
    state, tick = preview()
    live = state is None
    if live:
        state, tick = player.state, player.anim_tick
    f = player_view.frame(state, tick, player.vy if live else None)
    x, y, _ = player_view.origin(player, state)
    pyxel.rectb(x, y, SPRITE_W, SPRITE_H, 5)                  # sprite cell
    pyxel.rectb(player.x, player.y, player.w, player.h, 11)   # hitbox
    _text(2, 2, f"{'live' if live else 'preview'}: {state}  frame {f + 1}/{ANIMS[state][0]}  tick {tick}")
    _text(2, 10, f"x {player.x:.1f}  y {player.y:.1f}  vx {player.vx:.1f}  vy {player.vy:.2f}")
    _text(2, 18, (
        f"ground {player.on_ground}  air {player.in_air}  stand {player.standing}  "
        f"move {player.moving}  run {player.running}  block {player.blocking}  atk {player.attacking}"
    ))
    _text(2, 26, "F3 debug  [ ] animation")
