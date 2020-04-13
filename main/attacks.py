class Attack:
    def __init__(self, name, damage, levelRequired):

        self.name = name
        self.damage = damage
        self.levelRequired = levelRequired


class Growl(Attack):
    def __init__(self):
        super().__init__(name="Growl", damage=10, levelRequired=1)


class ThunderShock(Attack):
    def __init__(self):
        super().__init__(name="Thundershock", damage=30, levelRequired=3)


class TailWhip(Attack):
    def __init__(self):
        super().__init__(name="Tail Whip", damage=30, levelRequired=3)
