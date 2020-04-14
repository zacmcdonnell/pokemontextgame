"""Describes the tiles in the world space."""

import items, enemies, actions, world, dialoge, pokemon, util
from player import Player
import random, os


class MapTile:
    """The base class for a tile within the world space"""

    def __init__(self, x, y):
        """Creates a new tile.

        :param x: the x-coordinate of the tile
        :param y: the y-coordinate of the tile
        """
        self.x = x
        self.y = y

    def intro_text(self):
        """Information to be displayed when the player moves into this tile."""
        raise NotImplementedError()

    def display_dialoge(self, the_player):
        """Print the dialoge of the npc"""
        pass

    def modify_player(self, the_player):
        """Process actions that change the state of the player."""
        pass

    def adjacent_moves(self):

        directions = {
            actions.MoveNorth(): [self.x, self.y - 1],
            actions.MoveSouth(): [self.x, self.y + 1],
            actions.MoveEast(): [self.x + 1, self.y],
            actions.MoveWest(): [self.x - 1, self.y],
        }

        moves = []
        rooms = []
        for k, v in directions.items():
            room = world.tile_exists(v[0], v[1])

            if room != None:
                moves.append(k)
                rooms.append(room.__str__())
        return moves, rooms

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves, rooms = self.adjacent_moves()

        return moves, rooms


class Bedroom(MapTile):
    def intro_text(self):
        return """You wake up with dreary eyes and get out of bed.
Breakfast is in the living room"""

    def __str__(self):
        return "Bedroom"


class LivingRoom(MapTile):
    def intro_text(self):
        return "You walk into the living room as mum stands by the stove cooking eggs"

    def display_dialoge(self, the_player):
        return dialoge.livingRoomDialog

    def __str__(self):
        return "Living room"


class CousinsHouse(MapTile):
    def intro_text(self):
        return "You open the door to your couin BLUE's house and see his sister kniting"

    def display_dialoge(self, the_player):
        return f"BLUE'S SISTER: Hi {the_player.name}! BLUE is out at Grandpa's lab."

    def __str__(self):
        return "Blue's house"


class ProfsLab(MapTile):
    unlocked = False
    tutorial = True

    def intro_text(self):
        return (
            "You walk into a massive labratory and the scientist greet you as you enter"
        )

    def display_dialoge(self, the_player):
        if ProfsLab.unlocked and ProfsLab.tutorial:
            dialoge.slow_type("BLUE: Gramps! I'm fed up with waiting!")
            input()
            return dialoge.profOak
        elif ProfsLab.unlocked and ProfsLab.tutorial == False:
            return dialoge.profOak2
        else:
            return f"BLUE: \nYo {the_player.name} Gramps isn't around? I ran here cos' he said he had a pokemon for me."

    def available_actions(self):
        if ProfsLab.unlocked and ProfsLab.tutorial:
            ProfsLab.tutorial = False
            return [actions.Take(pokemon.Pikachu())], ["PIKACHU"]
        else:
            return self.adjacent_moves()

    def __str__(self):
        return "Oak Pokemon Research lab"


class Battle(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)

    def displayHealth(self, health, maxHealth):
        healthDashes = maxHealth
        # Get the number to divide by to convert health to dashes (being 10)
        try:
            dashConvert = int(maxHealth / healthDashes)
            # Convert health to dash count: 80/10 => 8 dashes
            currentDashes = int(health / dashConvert)
            # Get the health remaining to fill as space => 12 spaces
            remainingHealth = healthDashes - currentDashes
            # Convert 8 to 8 dashes as a string:   "--------"
            healthDisplay = "-" * currentDashes
            # Convert 12 to 12 spaces as a string: "            "
            remainingDisplay = " " * remainingHealth
            percent = str(int((health / maxHealth) * 100)) + "%"
        except ZeroDivisionError:
            pass
        # Print out textbased healthbar
        print("   -Health   : |" + healthDisplay + remainingDisplay + "|")
        print("                ", percent, "remaining")

    def displayBattle(self, pokemon):
        print("\n------------------------------------------------------")
        print(pokemon.name.upper())
        print("\nSTATS:")
        # print("   -LEVEL", pokemon.level)
        self.displayHealth(pokemon.hp, pokemon.maxHp)


class TallGrass(Battle):
    def __init__(self, x, y, possiblePokemon, levelMIN, levelMAX, battleChance):
        super().__init__(x, y)
        self.possiblePokemon = possiblePokemon
        self.levelMIN = levelMIN
        self.levelMAX = levelMAX
        self.battleChance = battleChance

    def intro_text(self):
        return "You reach through the thick grass unable to see upahead"

    def getRandomPokemon(self):
        return random.choice(self.possiblePokemon)

    def battle(self, player):
        while self.fight:
            self.displayBattle(self.wildPokemon)
            self.displayBattle(self.currentPokemon)
            input()
            util.getActions(
                [
                    actions.Run(tile=self),
                    actions.Attack(wildPokemon=self.wildPokemon),
                    actions.ViewInventory(),
                ],
                ["Leave battle", "Select Attacks", "View Inventory"],
                player,
            )
            input()
            enemyAttack = self.wildPokemon.getHighestAttack()
            self.currentPokemon.hp -= enemyAttack.damage
            print(f"\n{self.wildPokemon.name} used {enemyAttack.name}!")

            if self.wildPokemon.hp <= 0:
                print(f"Enemy {self.wildPokemon.name} fainted!")
                self.fight = False
            elif self.currentPokemon.hp <= 0:
                print(f"oh no {self.currentPokemon.name} fainted!")
                player.hp = 0
                self.fight = False

    def modify_player(self, the_player):
        if random.randint(0, 1) > self.battleChance:
            self.currentPokemon = Player.get_current_pokemon(the_player)
            self.wildPokemon = self.getRandomPokemon()
            self.wildPokemon.maxHp = self.wildPokemon.hp
            self.currentPokemon.maxHp = self.currentPokemon.hp
            input(f"A wild {self.wildPokemon.name} has appeared")
            input(f"GO! {self.currentPokemon.name}!")
            self.fight = True

            self.battle(the_player)

        else:
            self.fight = False

    def __str__(self):
        return "Tall Grass"


class EasyTallGrass(TallGrass):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            possiblePokemon=[pokemon.Metapod(), pokemon.Evee()],
            levelMIN=2,
            levelMAX=4,
            battleChance=0.4,
        )


class MysteriousPath(MapTile):
    locked = True

    def intro_text(self):
        return "As you approch the town gates a mysterious path leads into the distance and you wonder what lies ahead"

    def display_dialoge(self, the_player):
        if MysteriousPath.locked:
            ProfsLab.unlocked = True
            return dialoge.mysteriousPathDialog

    def available_actions(self):
        if MysteriousPath.locked:
            MysteriousPath.locked = False
            return [actions.FollowProfOak()], ["Oak Pokemon Research lab"]
        else:
            return self.adjacent_moves()

    def __str__(self):
        return "Mysterious Path"


class PaletTown(MapTile):
    def intro_text(self):
        return "Shades of your journey await.."

    def __str__(self):
        return "Palet Town"


class ViridianCity(MapTile):
    def intro_text(self):
        return "The eternally Green Paradise"

    def __str__(self):
        return "Viridian City"


class TownPath(MapTile):
    def intro_text(self):
        return "You walk along the path"

    def __str__(self):
        return "Path"


class Pond(MapTile):
    def intro_text(self):
        return "You walk past a picturesque pond"

    def __str__(self):
        return "Pond"


class FlowerPatch(MapTile):
    def intro_text(self):
        return "A field of flowers spans as far as the eye can see "

    def __str__(self):
        return "Flower Patch"


class PokeMart(MapTile):
    def intro_text(self):
        return "A field of flowers spans as far as the eye can see "

    def __str__(self):
        return "Poke Mart"


class PokeCenter(MapTile):
    def intro_text(self):
        return "A field of flowers spans as far as the eye can see "

    def __str__(self):
        return "Poke Center"


'''
class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """

    def modify_player(self, player):
        # Room has no action on player
        pass


class StartingRoom(MapTile):
    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """


class LootRoom(MapTile):
    """A room that adds something to the player's inventory"""

    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, the_player):
        the_player.inventory.append(self.item)

    def modify_player(self, the_player):
        self.add_loot(the_player)


class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())

    def intro_text(self):
        return """
        You notice something shiny in the corner.
        It's a dagger! You pick it up.
        """


class Find5GoldRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Gold(5))

    def intro_text(self):
        return """
        Someone dropped a 5 gold piece. You pick it up.
        """


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print(
                "Enemy does {} damage. You have {} HP remaining.".format(
                    self.enemy.damage, the_player.hp
                )
            )

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Run(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """


class OgreRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ogre())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            An ogre is blocking your path!
            """
        else:
            return """
            A dead ogre reminds you of your triumph.
            """


class SnakePitRoom(MapTile):
    def intro_text(self):
        return """
        You have fallen into a pit of deadly snakes!

        You have died!
        """

    def modify_player(self, player):
        player.hp = 0


class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!


        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True
'''
