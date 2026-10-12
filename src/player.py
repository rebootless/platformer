"""Player state, movement physics and animation state."""

from .combo import Combo
from .config import TILE
from .input import Controls
from .player_config import (
    GRAVITY, JUMP_SPEED, MAX_FALL, PLAYER_H, PLAYER_W, RUN_SPEED, WALK_SPEED,
)
from .world import box_hits


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.dir = 1            # facing: 1 right, -1 left
        # State flags, always 0 or 1
        self.on_ground = 0
        self.in_air = 1
        self.standing = 0       # on the ground and doing nothing
        self.moving = 0
        self.running = 0
        self.blocking = 0
        self.attacking = 0
        self.combo = Combo()
        self.state = "idle"     # animation name, see anims.ANIMS
        self.anim_tick = 0      # frames spent in the current state

    @property
    def w(self):
        return PLAYER_W

    @property
    def h(self):
        return PLAYER_H

    def update(self, c: Controls):
        if self.on_ground:
            self._ground(c)
        if not self.on_ground:
            # In the air: vx stays whatever it was at takeoff; no attack or block
            self.combo.cancel()
            self.blocking = 0
            self.vy = min(self.vy + GRAVITY, MAX_FALL)

        self._move_x()
        self._move_y()
        self._probe_ground()
        self._update_flags()
        self._animate()
        self.combo.update()

    def _ground(self, c):
        if c.attack:
            self.combo.press()
        move = c.right - c.left
        if self.combo.active:
            self.blocking = 0
            self.vx = 0.0       # mid-swing: rooted, facing locked
            return
        if move:
            self.dir = move
        self.blocking = int(c.block)
        if self.blocking:
            self.vx = 0.0       # shield up: can turn, can't move or jump
            return
        self.vx = move * (RUN_SPEED if c.run else WALK_SPEED)
        if c.jump:
            # Direction is fixed at takeoff - no air control
            self.vy = -JUMP_SPEED
            self.on_ground = 0

    def _update_flags(self):
        self.in_air = 1 - self.on_ground
        self.moving = int(self.vx != 0)
        self.running = int(abs(self.vx) > WALK_SPEED)
        self.attacking = int(self.combo.active)
        self.standing = int(
            self.on_ground and not (self.moving or self.blocking or self.attacking)
        )

    def _animate(self):
        """Pick the animation from the flags, highest priority first."""
        if self.in_air:
            state = "jump"
        elif self.attacking:
            state = self.combo.name
        elif self.blocking:
            state = "block"
        elif self.running:
            state = "run"
        elif self.moving:
            state = "walk"
        else:
            state = "idle"
        if state == self.state:
            self.anim_tick += 1
        else:
            self.state = state
            self.anim_tick = 0

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
        self.on_ground = int(self.vy >= 0 and box_hits(self.x, self.y + 1, self.w, self.h))
