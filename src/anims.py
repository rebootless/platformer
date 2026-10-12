"""Hero sprites and animations: sheet geometry, frame counts and timing.

Sheets are assets/hero_<name>.png: 64x48 cells, 4 per row, feet on the bottom
row, hero faces right. They need the extended palette in assets.pyxpal
(colour 0 is transparent).
"""

from pathlib import Path

SPRITES = str(Path(__file__).resolve().parent.parent / "assets")
SPRITE_W = 64
SPRITE_H = 48
SPRITE_FEET_X = 29      # column of the hero's feet inside a cell (facing right)
FEET_X = {              # sheets drawn with the hero shifted ~3px to the right
    "attack_first": 32,
    "attack_second": 32,
    "attack_third": 32,
}
SPRITE_COLKEY = 0

# name: (frames, ticks per frame, loop)
ANIMS = {
    "idle": (7, 8, True),
    "walk": (8, 7, True),
    "run": (8, 5, True),
    "jump": (5, 8, False),          # in game the frame comes from vy (JUMP_VY); ticks are for the debug preview
    "block": (6, 4, False),
    "damage": (4, 4, False),
    "dying": (12, 6, False),
    "attack_first": (6, 4, False),
    "attack_second": (5, 4, False),
    "attack_third": (6, 4, False),
}
HOLD = {"block": 1}     # frame to stay on once reached (shield stays up)
ATTACKS = ("attack_first", "attack_second", "attack_third")
# vy thresholds between jump frames: launch, rise, apex, fall, fast fall
JUMP_VY = (-2.0, -0.5, 0.5, 2.0)
