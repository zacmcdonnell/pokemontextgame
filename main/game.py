import world
from player import Player
import os
import dialoge


class Game:
    def __init__(self):
        self.gamePlaying = True
        world.load_tiles()
        self.player = Player()
        # self.start()
        self.main()

    def getActions(self):
        print("\nChoose an action:\n")
        available_actions = self.room.available_actions()
        for action in available_actions:
            print(action)
        action_input = input("Action: ")
        for action in available_actions:
            if action_input == action.hotkey:
                os.system("cls")
                self.player.do_action(action, **action.kwargs)
                break

    def main(self):
        while self.gamePlaying:
            if not self.player.is_alive() and not self.player.victory:
                print("ded")
            else:
                self.room = world.tile_exists(
                    self.player.location_x, self.player.location_y
                )
                print(self.room.__str__().upper().center(60, "-"))
                print(self.room.intro_text())
                input("...")
                self.room.modify_player(self.player)
                self.getActions()
                input("...")
                os.system("cls")

    def start(self):
        # intialise the game and display welcome screen
        os.system("cls")

        message = dialoge.tutorial.split("\n")
        for i in range(len(message)):
            print("WELCOME TO POKEMON".center(60, "-"))
            print()
            print("PROF. OAK:")
            dialoge.slow_type(message[i])

            if i == 7:
                self.player.name = input("> ")
                dialoge.slow_type("Right! So your name is " + self.player.name + "!")
            elif i == 10:
                name = input()
                dialoge.slow_type(
                    "That's right! I remember now! His name is " + name + "!"
                )
            input()
            os.system("cls")


if __name__ == "__main__":
    Game()
