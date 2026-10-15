import pyxel

from .sprites import HERO

# vy thresholds between jump frames: launch, rise, apex, fall, fast fall
JUMP_VY = (-2.0, -0.5, 0.5, 2.0)

_sheet = None


def load():
    # Load the hero spritesheet.
    global _sheet
    _sheet = pyxel.Image.from_image(str(HERO.path))


def frame(state, tick, vy=None):
    if state == "jump" and vy is not None:
        return sum(vy > t for t in JUMP_VY)
    return HERO.anims[state].frame(tick)


def origin(player, state):
    flip = player.dir != HERO.faces
    feet_x = HERO.feet(state)
    if flip:
        feet_x = HERO.w - feet_x
    x = int(player.x + player.w / 2 - feet_x)
    y = int(player.y + player.h - HERO.h)
    return x, y, flip


def draw(player, state=None, tick=0):
    # Draw the player's own animation, or `state` at `tick` when given (debug).
    live = state is None
    if live:
        state, tick = player.state, player.anim_tick
    f = frame(state, tick, player.vy if live else None)
    x, y, flip = origin(player, state)
    pyxel.blt(
        x, y, _sheet,
        f * HERO.w, HERO.anims[state].row * HERO.h,
        -HERO.w if flip else HERO.w, HERO.h,
        HERO.colkey,
    )
