from .sprites import HERO

ATTACKS = ("attack_first", "attack_second", "attack_third")


class Combat:
    def __init__(self):
        self.step = None        # index into ATTACKS, None when not attacking
        self.tick = 0           # frames spent in the current swing
        self.queued = False     # attack was pressed during the current swing

    @property
    def active(self):
        return self.step is not None

    @property
    def name(self):
        return ATTACKS[self.step]

    def press(self):
        if self.step is None:
            self.step, self.tick, self.queued = 0, 0, False
        elif self.step < len(ATTACKS) - 1:
            self.queued = True  # a press during the last hit is ignored

    def cancel(self):
        self.step = None

    def update(self):
        if self.step is None:
            return
        self.tick += 1
        if self.tick < HERO.anims[ATTACKS[self.step]].length:
            return
        if self.queued:
            self.step += 1
            self.tick, self.queued = 0, False
        else:
            self.step = None
