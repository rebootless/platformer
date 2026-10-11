"""Keyboard / gamepad bindings and per-frame input snapshot."""

from dataclasses import dataclass

import pyxel

LEFT = (pyxel.KEY_LEFT, pyxel.KEY_A, pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
RIGHT = (pyxel.KEY_RIGHT, pyxel.KEY_D, pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)
DOWN = (pyxel.KEY_DOWN, pyxel.KEY_S, pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)
JUMP = (pyxel.KEY_Z, pyxel.KEY_SPACE, pyxel.GAMEPAD1_BUTTON_A)


@dataclass(frozen=True)
class Controls:
    left: bool = False
    right: bool = False
    down: bool = False
    jump: bool = False  # edge-triggered: True only on the press frame


def _held(buttons):
    return any(pyxel.btn(b) for b in buttons)


def _pressed(buttons):
    return any(pyxel.btnp(b) for b in buttons)


def read():
    return Controls(
        left=_held(LEFT),
        right=_held(RIGHT),
        down=_held(DOWN),
        jump=_pressed(JUMP),
    )
