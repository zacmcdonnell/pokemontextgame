"""Defines the enemies in the game"""
import random, attacks


class WildPokemon:
    """A base class for all enemies"""

    def __init__(self, name, hp, attack, speed, possibleAttacks=None):
        """Creates a new enemy

        :param name: the name of the enemy
        :param hp: the hit points of the enemy
        """
        self.name = name
        self.hp = hp
        self.attack = attack
        self.speed = speed  # THIS DETERMINES WHO ATTACKS FIRST
        self.possibleAttacks = possibleAttacks

    def is_alive(self):
        return self.hp > 0

    def getHighestAttack(self):
        for i in self.possibleAttacks:
            attack = 0
            if i.damage > attack:
                attack = i
        return attack


class Pikachu(WildPokemon):
    def __init__(self):
        super().__init__(
            name="Pikachu",
            hp=35,
            attack=55,
            speed=90,
            possibleAttacks=[attacks.Growl(), attacks.ThunderShock()],
        )


class Pidgey(WildPokemon):
    def __init__(self):
        super().__init__(
            name="Pikachu",
            hp=35,
            attack=55,
            speed=90,
            possibleAttacks=[attacks.Growl(), attacks.ThunderShock()],
        )


class Rattata(WildPokemon):
    def __init__(self):
        super().__init__(
            name="Pikachu",
            hp=35,
            attack=55,
            speed=90,
            possibleAttacks=[attacks.Growl(), attacks.ThunderShock()],
        )


class Spearow(WildPokemon):
    def __init__(self):
        super().__init__(
            name="Pikachu",
            hp=35,
            attack=55,
            speed=90,
            possibleAttacks=[attacks.Growl(), attacks.ThunderShock()],
        )


class Evee(WildPokemon):
    def __init__(self):
        super().__init__(
            name="Eevee",
            hp=55,
            attack=55,
            speed=55,
            possibleAttacks=[attacks.Growl(), attacks.ThunderShock()],
        )


class Metapod(WildPokemon):
    def __init__(self):
        super().__init__(
            name="Metapod",
            hp=50,
            attack=20,
            speed=30,
            possibleAttacks=[attacks.Growl(), attacks.ThunderShock()],
        )
