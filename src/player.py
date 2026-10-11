"""Player state and movement physics."""

from .config import (
    CROUCH_H, GRAVITY, JUMP_SPEED, MAX_FALL, PLAYER_H, PLAYER_W, TILE, WALK_SPEED,
)
from .input import Controls
from .world import box_hits


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.dir = 1            # facing: 1 right, -1 left
        self.on_ground = False
        self.crouching = False

    @property
    def w(self):
        return PLAYER_W

    @property
    def h(self):
        return CROUCH_H if self.crouching else PLAYER_H

    def update(self, c: Controls):
        if self.on_ground:
            self._set_crouch(c.down)
            self._ground_move(c)
            if c.jump and not self.crouching:
                # Direction is fixed at takeoff - no air control
                self.vy = -JUMP_SPEED
                self.on_ground = False
        # In the air: vx stays whatever it was at takeoff

        if not self.on_ground:
            self.vy = min(self.vy + GRAVITY, MAX_FALL)

        self._move_x()
        self._move_y()
        self._probe_ground()

    def _ground_move(self, c):
        # Ground movement is locked while crouching
        move = (c.right - c.left) if not self.crouching else 0
        if move:
            self.dir = move
        self.vx = move * WALK_SPEED

    def _set_crouch(self, crouch):
        if crouch == self.crouching:
            return
        # Keep feet in place when height changes
        self.y += self.h - (CROUCH_H if crouch else PLAYER_H)
        self.crouching = crouch

    def _move_x(self):
        nx = self.x + self.vx
        if not box_hits(nx, self.y, self.w, self.h):
            self.x = nx
        else:
            self.vx = 0.0

    def _move_y(self):
        ny = self.y + self.vy
        if not box_hits(self.x, ny, self.w, self.h):
            self.y = ny
            return
        if self.vy > 0:
            # Landed: snap feet to the top of the tile
            self.y = ((int(ny + self.h - 1) // TILE) * TILE) - self.h
        else:
            self.y = ((int(ny) // TILE) + 1) * TILE  # bumped the ceiling
        self.vy = 0.0

    def _probe_ground(self):
        """Is there a floor right under the feet?"""
        self.on_ground = self.vy >= 0 and box_hits(self.x, self.y + 1, self.w, self.h)
