class Stats:
    def __init__(self, max_hp):
        self.max_hp = max_hp
        self.hp = max_hp

    @property
    def alive(self):
        return self.hp > 0

    def damage(self, amount):
        # Returns the HP actually lost.
        lost = min(amount, self.hp)
        self.hp -= lost
        return lost

    def heal(self, amount):
        # Returns the HP actually restored.
        gained = min(amount, self.max_hp - self.hp)
        self.hp += gained
        return gained

    def reset(self):
        self.hp = self.max_hp