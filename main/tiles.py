"""Describes the tiles in the world space."""

import items, enemies, actions, world, dialoge, os, game


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

    def modify_player(self, the_player):
        """Process actions that change the state of the player."""
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())

        return moves

    def displayDialoge(self, locName, message, talking):
        message = message.split("\n")
        for i in range(len(message)):
            os.system("cls")
            print(locName.upper().center(60, "-"))

            print(talking.upper() + ":")
            dialoge.slow_type(message[i])
            input()


class Bedroom(MapTile):
    def intro_text(self):
        return """You wake up with dreary eyes and get out of bed.
Breakfast is in the living room"""

    def modify_player(self, the_player):
        # Room has no action on player
        pass

    def __str__(self):
        return "Bedroom"


class LivingRoom(MapTile):
    def intro_text(self):
        return "You walk into the living room as mum stands by the stove cooking eggs"

    def modify_player(self, the_player):
        print("wdha")

        self.displayDialoge(self.__str__(), dialoge.livingRoomDialog, "MUM")

    def __str__(self):
        return "Living room"


class CousinsHouse(MapTile):
    def intro_text(self):
        return "You open the door to your couin BLUE's house and see his sister kniting"

    def modify_player(self, the_player):
        dialoge.slow_type(
            f"BLUE'S SISTER: Hi {the_player.name}! BLUE is out at Grandpa's lab."
        )

    def __str__(self):
        return "Blue's house"


class ProfsLab(MapTile):
    locked = True

    def intro_text(self):
        return (
            "You walk into a massive labratory and the scientist greet you as you enter"
        )

    def modify_player(self, the_player):
        if ProfsLab.locked:
            dialoge.slow_type(
                f"BLUE: Yo {the_player.name} Gramps isn't around? I ran here cos' he said he had a pokemon for me."
            )

        else:
            print("yeet")

    def __str__(self):
        return "Oak Pokemon Research lab"


class MysteriousPath(MapTile):
    def intro_text(self):
        return "As you approch the town gates a mysterious path leads into the distance and you wonder what lies ahead"

    def modify_player(self, the_player):
        self.displayDialoge(self.__str__(), dialoge.mysteriousPathDialog, "PROF OAK")
        the_player.move(0,3)
        ProfsLab.locked = False

    def __str__(self):
        return "Mysterious Path"


class TownPath(MapTile):
    def intro_text(self):
        return "You walk along the path"

    def modify_player(self, the_player):
        pass

    def __str__(self):
        return "Path"


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
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
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
