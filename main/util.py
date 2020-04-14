import os
import dialoge


def welcome(player):
    # intialise the game and display welcome screen
    os.system("cls")

    message = dialoge.tutorial.split("\n")
    for i in range(len(message)):
        print("WELCOME TO POKEMON".center(60, "-"))
        print()
        print("PROF. OAK:")
        dialoge.slow_type(message[i])

        if i == 7:
            player.name = input("> ")
            dialoge.slow_type("Right! So your name is " + player.name + "!")
        elif i == 10:
            name = input()
            dialoge.slow_type("That's right! I remember now! His name is " + name + "!")
        input()
        os.system("cls")


def getActions(available_actions, toolTips, player):
    print("\nChoose an action:\n")
    for action, toolTip in zip(available_actions, toolTips):
        print(f"{action} ({toolTip})")

    action_input = input("Action: ")
    for action in available_actions:
        if action_input == action.hotkey:
            os.system("cls")
            player.do_action(action, **action.kwargs)
            break


def displayDialoge(roomName, message):
    if isinstance(message, dialoge.dialogue):
        talking = message.talking
        message = message.string.split("\n")
        for i in message:
            os.system("cls")
            print(roomName.upper().center(60, "-"))
            print(talking.upper() + ":")
            dialoge.slow_type(i)
            input()
    else:
        if message:
            dialoge.slow_type(message)
            input()
        else:
            pass
