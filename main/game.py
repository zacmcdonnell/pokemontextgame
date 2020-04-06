import world
from player import Player
import os
import dialoge


def play():
    os.system("cls")
    world.load_tiles()
    player = Player()
    start(player)
    room = world.tile_exists(player.location_x, player.location_y)
    room.intro_text(player)
    while player.is_alive() and not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        room.modify_player(player)
        # Check again since the room could have changed the player's state
        if player.is_alive() and not player.victory:
            print("Choose an action:\n")
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)
            action_input = input("Action: ")
            for action in available_actions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    break


def start(player):
    # intialise the game and display welcome screen
    os.system("cls")
    message = dialoge.tutorial.split("\n")
    for i in range(len(message)):
        # print(i)
        print("WELCOME TO POKEMON".center(70, "-"))
        print()
        print("PROFFESSOR OAK:", message[i])
        if i == 7:
            player.name = input("> ")
            print("Right! So your name is " + player.name + "!")
        elif i == 10:
            name = input()
            print("That's right! I remember now! His name is " + name + "!")
        input()
        os.system("cls")


if __name__ == "__main__":
    play()
