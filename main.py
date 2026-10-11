# Show command help
# .venv/bin/pyxel

# Open the resource editor
# .venv/bin/pyxel edit assets.pyxres

# Run the game
# .venv/bin/pyxel run main.py

import pyxel

COLLISION_TILES = [
    (1, 0), (2, 0), (2, 1),
    (0, 1), (1, 1), (3, 0),
    (4, 0), (3, 1), (4, 1),
]

# Physics (px per frame at 60 fps)
WALK_SPEED = 1.0
JUMP_SPEED = 3.0
GRAVITY = 0.15
MAX_FALL = 4.0

PLAYER_W = 10
PLAYER_H = 24
CROUCH_H = 16


def solid(px, py):
    # True if the pixel position is inside a collision tile
    if px < 0 or px >= 256:
        return True  # screen edges act as walls
    if py < 0:
        return False
    return pyxel.tilemaps[0].pget(px // 8, py // 8) in COLLISION_TILES


def box_hits(x, y, w, h):
    return any(
        solid(px, py)
        for px in (int(x), int(x + w - 1))
        for py in (int(y), int(y + h // 2), int(y + h - 1))
    )


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        # facing: 1 right, -1 left
        self.dir = 1
        self.on_ground = False
        self.crouching = False

    @property
    def h(self):
        return CROUCH_H if self.crouching else PLAYER_H

    def update(self, left, right, down, jump_pressed):
        if self.on_ground:
            self._set_crouch(down)

            # Ground movement is locked while crouching
            move = (right - left) if not self.crouching else 0
            if move:
                self.dir = move
            self.vx = move * WALK_SPEED

            if jump_pressed and not self.crouching:
                # Direction is fixed at takeoff - no air control
                self.vy = -JUMP_SPEED
                self.on_ground = False
        # In the air: vx stays whatever it was at takeoff

        if not self.on_ground:
            self.vy = min(self.vy + GRAVITY, MAX_FALL)

        # Horizontal move with collision
        nx = self.x + self.vx
        if not box_hits(nx, self.y, PLAYER_W, self.h):
            self.x = nx
        else:
            self.vx = 0.0

        # Vertical move with collision
        ny = self.y + self.vy
        if not box_hits(self.x, ny, PLAYER_W, self.h):
            self.y = ny
        else:
            if self.vy > 0:
                # Landed: snap feet to the top of the tile
                self.y = ((int(ny + self.h - 1) // 8) * 8) - self.h
            else:
                self.y = ((int(ny) // 8) + 1) * 8  # bumped the ceiling
            self.vy = 0.0

        # Ground probe
        self.on_ground = self.vy >= 0 and box_hits(self.x, self.y + 1, PLAYER_W, self.h)

    def _set_crouch(self, crouch):
        if crouch == self.crouching:
            return
        # Keep feet in place when height changes
        self.y += self.h - (CROUCH_H if crouch else PLAYER_H)
        self.crouching = crouch

    def draw(self):
        pyxel.rect(self.x, self.y, PLAYER_W, self.h, 8)


def key_or_pad(keys, pad_buttons, pressed=False):
    f = pyxel.btnp if pressed else pyxel.btn
    return any(f(k) for k in (*keys, *pad_buttons))


class App:
    def __init__(self):
        pyxel.init(256, 240, title="platformer", fps=60)
        pyxel.load("assets.pyxres")
        self.player = Player(16, 70)
        pyxel.run(self.update, self.draw)

    def update(self):
        left = key_or_pad((pyxel.KEY_LEFT, pyxel.KEY_A), (pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,))
        right = key_or_pad((pyxel.KEY_RIGHT, pyxel.KEY_D), (pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,))
        down = key_or_pad((pyxel.KEY_DOWN, pyxel.KEY_S), (pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,))
        jump = key_or_pad((pyxel.KEY_Z, pyxel.KEY_SPACE), (pyxel.GAMEPAD1_BUTTON_A,), pressed=True)
        self.player.update(left, right, down, jump)

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 256, 240, 0)
        self.player.draw()


if __name__ == "__main__":
    App()
