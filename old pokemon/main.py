import os
import pokemonData as data
from player import player
import random


class pokemon:
    def __init__(self, name, level, health, maxHealth, experience, possibleAttacks, attack, defense, speed, special):
        self.name = name
        self.level = level
        self.health = health
        self.maxHealth = maxHealth
        self.experience = experience
        self.possibleAttacks = possibleAttacks
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.special = special

    def displayHealth(self, health, maxHealth):
        healthDashes = maxHealth
        # Get the number to divide by to convert health to dashes (being 10)
        dashConvert = int(maxHealth/healthDashes)
        # Convert health to dash count: 80/10 => 8 dashes
        currentDashes = int(health/dashConvert)
        # Get the health remaining to fill as space => 12 spaces
        remainingHealth = healthDashes - currentDashes
        # Convert 8 to 8 dashes as a string:   "--------"
        healthDisplay = '-' * currentDashes
        # Convert 12 to 12 spaces as a string: "            "
        remainingDisplay = ' ' * remainingHealth
        percent = str(int((health/maxHealth)*100)) + "%"
        # Print out textbased healthbar
        print("   -Health   : |" + healthDisplay + remainingDisplay + "|")
        print('                ', percent, 'remaining')

    def displayBattle(self):
        print('\n------------------------------------------------------')
        print(self.name.upper())
        print('\nSTATS:')
        print("   -LEVEL", self.level)
        self.displayHealth(self.health, self.maxHealth)


pikauchu = pokemon('pikauchu', 5, 19, 20, 0, [
                   "THUNDERSHOCK", "GROWL"], 12, 9, 15, 10)


currentPokemon = pikauchu


class enemyPokemon(pokemon):

    def fight(self):

        for i in currentPokemon.possibleAttacks:
            print(' -', i.upper())

        userInput = input("> ").lower()

        if userInput == 'thundershock':
            self.health -= 5
            print("DAMMMM U GOTEM GOOD")
            input()

    def options(self):
        global fight
        print('WHAT DO YOU DO?:')
        options = ['fight', 'run', 'item', 'switch']
        for i in options:
            print(' -', i.upper())

        userInput = input("> ").lower()

        if userInput == 'fight':
            self.fight()

        elif userInput == 'run':
            fight = False
            print('you got away saftley')
        elif userInput == 'item':
            # DO THIS SOON
            # showBackpack()
            print("SHOW BACKPACK FUNCTION")
        elif 'switch':
            # SHOW POKEMON
            print('SHOW POKEMON FUNCTION')

    def battle(self):
        global fight
        os.system('cls')

        fight = True
        print('A wild', self.name, 'has appeared')
        input('......')
        while fight:
            os.system('cls')
            currentPokemon.displayBattle()
            self.displayBattle()
            input('......')
            self.options()

    def chooseAttack(self):
        random.choice(self.possibleAttacks)


jojo = enemyPokemon('EEVEE', 5, 19, 20, 0, [
    "THUNDERSHOCK", "GROWL"], 12, 9, 15, 10)


class area:
    def __init__(self, locations):
        self.locations = locations

    def moveArea(self, newArea):
        player.area = PokeMonWorld.get(newArea)

    def moveLocation(self):
        print('Go To:')
        for i in self.locations:
            if i != player.location:
                print(' -', i.capitalize())
        userInput = input("> ").lower()
        for i in self.locations:
            if userInput == i:
                player.location = i
                return True


class location:
    def __init__(self, inputDialoge, talking):
        try:
            self.dialoge = inputDialoge.split('\n')
        except:
            self.dialoge = inputDialoge
        self.talking = talking

    def displayDialoge(self):
        for i in range(len(self.dialoge)):
            print(player.location.upper().center(70, '-'))
            print(self.talking.upper() + ':', self.dialoge[i])
            input()
            os.system('cls')

    def describeLocation(self):
        if self.moveLocation():
            os.system('cls')
            print("You have arrived at the",
                  player.location.capitalize())
            input('.....')
            os.system('cls')
            self.locations.get(player.location).displayDialoge()
            input('.....')
        else:
            os.system('cls')


class House:
    def __init__(self):
        self.locations = {
            'living room': data.location(data.livingRoomDialog, 'mum'),
            'bedroom': data.location(None, None)
        }
        self.specifc()

    def specifc(self):
        if player1.location == 'living room':
            print('YOU WALK OUTSIDE AND YOU EYES ARE BLINDED BY SUNLIGHT'.center(70))
            input()
            player1.moveArea('Palet Town')


PokeMonWorld = {
    'house': area(),

    'Palet Town': area({
        'oak pokemon research lab': data.location(data.profLabDialog, "blue"),
        "cousins' house": data.location(data.bluesHouseDialog, "blue's sister"),
        'your house': data.location(None, None),
        'mysterious path': data.location(data.mysteriousPathDialog, 'PROFFESSOR OAK:')
    })
}

print('PALET TOWN'.center(70, '-'))
print('SHADES OF YOUR JOURNEY AWAIT'.center(70))


class Game:
    def __init__(self):
        self.start()

    def start(self):
        # intialise the game and display welcome screen
        os.system('cls')
        dialoge = data.tutorial.split('\n')
        for i in range(len(dialoge)):
            # print(i)
            print("WELCOME TO POKEMON".center(70, '-'))
            print()
            print('PROFFESSOR OAK:', dialoge[i])
            if i == 7:
                player.name = input('> ')
                print('Right! So your name is ' + player.name + '!')
            elif i == 10:
                name = input()
                print("That's right! I remember now! His name is " +
                      name + '!')
            input()
            os.system('cls')

    def MainGame(self):
        while True:
            player.moveLocation()

            # program entry point
if __name__ == '__main__':
    # assign the game class to the master variable
    master = Game()
    # call the mainGame()
    master.MainGame()
