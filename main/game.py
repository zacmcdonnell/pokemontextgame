import world
from player import Player
import os
import dialoge
import util


class Game:
    def __init__(self):
        world.load_tiles()
        self.player = Player()
        util.welcome(self.player)

        self.main()

    def gamePlaying(self):
        if self.player.victory:
            if self.player.is_alive():
                return True
            else:
                print("Sad you died ")
        print("you won")

    def main(self):

        while self.gamePlaying:
            self.room = world.tile_exists(
                self.player.location_x, self.player.location_y
            )
            print(self.room.__str__().upper().center(60, "-"))
            print(self.room.intro_text())
            input()
            util.displayDialoge(
                self.room.__str__(), self.room.display_dialoge(self.player)
            )

            self.room.modify_player(self.player)
            available_actions, locations = self.room.available_actions()
            util.getActions(available_actions, locations, self.player)
            input("...")
            os.system("cls")


if __name__ == "__main__":
    Game()
