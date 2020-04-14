import random, os
import items, world
import pokemon
import util


class Player:
    def __init__(self):
        self.name = "Yellow"
        self.inventory = [items.Gold(15), items.Rock()]
        self.hp = 100
        self.location_x, self.location_y = world.starting_position
        self.pokemon = [pokemon.Pikachu()]
        self.victory = False

    def is_alive(self):
        return self.hp > 0

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def print_inventory(self):
        for item in self.inventory:
            print(item, "\n")

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def get_current_pokemon(self):
        for i in self.pokemon:
            if i.hp > 0:
                return i
            else:
                print("no more alive pokemon")
                self.hp = 0

    def capturePokemon(self, wildPokemon):
        captureChance = 0.5
        if wildPokemon.hp < 20:
            captureChance += 0.3
        if random.randint(0, 1) > captureChance:
            print(f"Oh no {wildPokemon.name} got away")
        else:
            print(f"horray {wildPokemon.name} was caught!")
            self.pokemon.append(wildPokemon)

    def takeItem(self, item):
        self.inventory.append(item)
        print(f"{self.name} recived a {item.name}!")

    def followOak(self):
        self.location_x = 0
        self.location_y = 2

    def attack(self, wildPokemon):
        possibleAttacks = self.get_current_pokemon().possibleAttacks

        print("\nChoose an action:\n")

        for attack in possibleAttacks:
            print(f"{attack.name[0].lower()}: {attack.name} ")

        action_input = input("Action: ").lower()
        for action in possibleAttacks:
            if action_input == action.name[0].lower():
                print(f"\n{self.get_current_pokemon().name} used {action.name}!")
                action.attack(wildPokemon)

        """
    def attack(self, enemy):
        best_weapon = None
        max_dmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon):
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    best_weapon = i

        print("You use {} against {}!".format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))
    """

    def run(self, tile):
        print("Got away safetly!")
        tile.fight = False
