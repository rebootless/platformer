"""Sprite definitions: one block per spritesheet, data only.

Every sheet is assets/<file>: a grid of w x h cells, one animation per row,
frames left to right. All sheets share the extended palette in assets.pyxpal
(colour 0 is transparent).

Sheet:
  file    file name in assets/
  w, h    cell size in px
  feet_x  column of the feet inside a cell, facing `faces` (None: not needed)
  faces   direction the art looks: 1 right, -1 left
  colkey  transparent colour

Anim (one row of a sheet):
  row     row index in the sheet
  frames  number of frames in the row
  ticks   game ticks per frame (the game runs at 60 ticks per second)
  loop    repeat after the last frame, else stay on it
  hold    frame to stay on once reached (e.g. shield stays up), None: none
  feet_x  overrides Sheet.feet_x for this row
  hit     frames (0-based) on which the attack deals damage; () until used
  mirror  flip the row when facing the other way
  turn    turn row: play first to last when turning right, reversed when
          turning left (use with mirror=False)
  touch   deals damage on contact
"""

from dataclasses import dataclass, field
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent / "assets"


@dataclass(frozen=True)
class Anim:
    row: int
    frames: int
    ticks: int
    loop: bool = True
    hold: int | None = None
    feet_x: int | None = None
    hit: tuple = ()
    mirror: bool = True
    turn: bool = False
    touch: bool = False

    @property
    def length(self):
        return self.frames * self.ticks

    def frame(self, tick):
        i = tick // self.ticks
        if self.hold is not None:
            return min(i, self.hold)
        return i % self.frames if self.loop else min(i, self.frames - 1)


@dataclass(frozen=True)
class Sheet:
    file: str
    w: int
    h: int
    anims: dict = field(default_factory=dict)
    feet_x: int | None = None
    faces: int = 1
    colkey: int = 0

    @property
    def path(self):
        return DIR / self.file

    def feet(self, name):
        own = self.anims[name].feet_x
        return self.feet_x if own is None else own


# Feet column is 29; attack rows are drawn ~3px to the right.
HERO = Sheet(
    file="hero_64x48.png", w=64, h=48, feet_x=29, faces=1,
    anims={
        "idle":          Anim(row=0, frames=7,  ticks=8),
        "walk":          Anim(row=1, frames=8,  ticks=7),
        "run":           Anim(row=2, frames=8,  ticks=5),
        "jump":          Anim(row=3, frames=5,  ticks=8, loop=False),  # in game the frame comes from vy; ticks are for the debug preview
        "damage":        Anim(row=4, frames=4,  ticks=4, loop=False),
        "dying":         Anim(row=5, frames=12, ticks=6, loop=False),
        "attack_first":  Anim(row=6, frames=6,  ticks=4, loop=False, feet_x=32),
        "attack_second": Anim(row=7, frames=5,  ticks=4, loop=False, feet_x=32),
        "attack_third":  Anim(row=8, frames=6,  ticks=4, loop=False, feet_x=32),
        "block":         Anim(row=9, frames=6,  ticks=4, loop=False, hold=1),
    },
)

ANDROMALIUS = Sheet(
    file="balmer_andromalius_64x96.png", w=64, h=96, faces=1,
    anims={
        "move":        Anim(row=0, frames=8, ticks=6, touch=True),
        "move_attack": Anim(row=1, frames=8, ticks=6, touch=True),
        "turn":        Anim(row=2, frames=8, ticks=6, loop=False, mirror=False, turn=True, touch=True),
    },
)

MINION = Sheet(
    file="balmer_minion_48x64.png", w=48, h=64, faces=1,
    anims={
        "move_attack": Anim(row=0, frames=4, ticks=6, touch=True),
        "turn":        Anim(row=1, frames=1, ticks=6, loop=False, mirror=False, turn=True, touch=True),
    },
)

GOLEM = Sheet(
    file="golem_64x80.png", w=64, h=80, faces=1,
    anims={
        "idle":   Anim(row=0, frames=1, ticks=6, touch=True),
        "walk":   Anim(row=1, frames=7, ticks=6, touch=True),
        "attack": Anim(row=2, frames=6, ticks=6, loop=False, touch=True),  # stands still
    },
)

SWAMP_MONSTER = Sheet(
    file="swamp_monster_32x48.png", w=32, h=48, faces=1,
    anims={
        "move_attack": Anim(row=0, frames=4, ticks=6, touch=True),
    },
)

WARTAUR = Sheet(
    file="wartaur_80x64.png", w=80, h=64, faces=1,
    anims={
        "idle":   Anim(row=0, frames=1, ticks=6, touch=True),
        "walk":   Anim(row=1, frames=4, ticks=6, touch=True),
        "attack": Anim(row=2, frames=4, ticks=6, loop=False, touch=True),  # stands still
    },
)
