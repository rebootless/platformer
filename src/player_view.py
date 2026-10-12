"""Player rendering: spritesheet animations anchored to the feet."""

import pyxel

from .anims import (
    ANIMS, FEET_X, HOLD, JUMP_VY, SPRITE_COLKEY, SPRITE_FEET_X, SPRITE_H, SPRITE_W, SPRITES,
)

_sheets = {}


def load():
    """Load the hero spritesheets. Call after pyxel.load() so the palette is set."""
    for name in ANIMS:
        _sheets[name] = pyxel.Image.from_image(f"{SPRITES}/hero_{name}.png")


def frame(state, tick, vy=None):
    """Frame index of an animation. Pass vy to pick jump frames from vertical speed."""
    frames, ticks, loop = ANIMS[state]
    if state == "jump" and vy is not None:
        return sum(vy > t for t in JUMP_VY)
    i = tick // ticks
    if state in HOLD:
        return min(i, HOLD[state])
    return i % frames if loop else min(i, frames - 1)


def origin(player, state):
    """Top-left of the sprite cell on screen and whether it is mirrored."""
    flip = player.dir < 0
    feet_x = FEET_X.get(state, SPRITE_FEET_X)
    # Mirroring flips the cell around its centre, so mirror the feet column too
    if flip:
        feet_x = SPRITE_W - feet_x
    x = int(player.x + player.w / 2 - feet_x)
    y = int(player.y + player.h - SPRITE_H)
    return x, y, flip


def draw(player, state=None, tick=0):
    """Draw the player's own animation, or `state` at `tick` when given (debug)."""
    live = state is None
    if live:
        state, tick = player.state, player.anim_tick
    f = frame(state, tick, player.vy if live else None)
    x, y, flip = origin(player, state)
    pyxel.blt(
        x, y, _sheets[state],
        (f % 4) * SPRITE_W, (f // 4) * SPRITE_H,
        -SPRITE_W if flip else SPRITE_W, SPRITE_H,
        SPRITE_COLKEY,
    )
