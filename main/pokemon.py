"""Defines the enemies in the game"""
import random


class WildPokemon:
    """A base class for all enemies"""

    def __init__(self, name, hp, attack, speed):
        """Creates a new enemy

        :param name: the name of the enemy
        :param hp: the hit points of the enemy
        :param damage: the damage the enemy does with each attack
        """
        self.name = name
        self.hp = hp
        self.level = random.randint(1, 5)
        self.attack = attack
        self.speed = speed  # THIS DETERMINES WHO ATTACKS FIRST

    def is_alive(self):
        return self.hp > 0


class Pikachu(WildPokemon):
    def __init__(self):
        super().__init__(name="Pikachu", hp=35, attack=55, speed=90)


class Evee(WildPokemon):
    def __init__(self):
        super().__init__(name="Eevee", hp=55, attack=55, speed=55)


class Metapod(WildPokemon):
    def __init__(self):
        super().__init__(name="Metapod", hp=50, attack=20, speed=30)
