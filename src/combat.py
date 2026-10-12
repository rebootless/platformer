"""Three-hit attack chain: pressing attack during a swing queues the next hit."""

from .anims import ANIMS, ATTACKS


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
            self.queued = True      # a press during the last hit is ignored

    def cancel(self):
        self.step = None

    def update(self):
        """Advance one frame; the swing ends after its full animation has played."""
        if self.step is None:
            return
        self.tick += 1
        frames, ticks, _ = ANIMS[ATTACKS[self.step]]
        if self.tick < frames * ticks:
            return
        if self.queued:
            self.step += 1
            self.tick, self.queued = 0, False
        else:
            self.step = None
