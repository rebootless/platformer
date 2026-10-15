from dataclasses import dataclass

import pyxel

LEFT = (pyxel.KEY_LEFT, pyxel.KEY_A, pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
RIGHT = (pyxel.KEY_RIGHT, pyxel.KEY_D, pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)
JUMP = (pyxel.KEY_Z, pyxel.KEY_SPACE, pyxel.GAMEPAD1_BUTTON_A)
ATTACK = (pyxel.KEY_X,)
BLOCK = (pyxel.KEY_C,)
RUN = (pyxel.KEY_SHIFT,)


@dataclass(frozen=True)
class Controls:
    left: bool = False
    right: bool = False
    jump: bool = False    # edge-triggered: True only on the press frame
    attack: bool = False  # edge-triggered
    block: bool = False   # held
    run: bool = False     # held


def _held(buttons):
    return any(pyxel.btn(b) for b in buttons)


def _pressed(buttons):
    return any(pyxel.btnp(b) for b in buttons)


def read():
    return Controls(
        left=_held(LEFT),
        right=_held(RIGHT),
        jump=_pressed(JUMP),
        attack=_pressed(ATTACK),
        block=_held(BLOCK),
        run=_held(RUN),
    )
