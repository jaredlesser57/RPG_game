# Modify the program so that the exits is a dictionary rather than a list,
# with the keys being the numbers of the locations and the values being
# dictionaries holding the exits (as they do at present). No change should
# be needed to the actual code.

# Once that is working, create another dictionary that contains words that
# players may use. These words will be the keys, and their values will be
# a single letter that the program can use to determine which way to go.

import sys
from termcolor import colored, cprint
from colorama import init
init()
from time import sleep
import re
from os import system, name
import pygame


# match = re.search(r'[a-zA-Z0-9]', '123dfdf')


guide = """
When prompted to "Start your Journey", type in 'y' to begin
the game. At any point during the game, you can type 'i' which
will display your inventory contents. Certain items can be combined
to create new items. Type 'help' at any time to list commands.

Use the keys to move around as shown (not all rooms lead in all directions):

N (north)
S (south)
E (east)
W (west)


NOTE: DO NOT press the Q button (even though listed). This will end the game...
"""

 

print(colored(f"{guide}", 'green'))

music = input("Music on or off (on/off): ")
if music == 'on':   
    pygame.mixer.init()
    pygame.mixer.music.load("tension.wav")
    pygame.mixer.music.play(-1)
else:
    print("The music will be muted\n")

name = input("Enter in your name: ").title()
choose = input("Start your Journey (y/n)? ").lower()


 
intro = """
You are entering unknown territory. As you work your
way through the game, you will collect items. These items
will unlock new rooms and ensure a safe path to the end.
Good luck on your journey {}...
""".format(name)

commands = """

Commands listed below:

Display inventory - 'i'
Clear screen      - 'cls'
Display commands  - 'help'

"""

inventory = []

 

locations = {0: "You've fallen into a pit of spikes!",
             1: "You are standing at the end of a road before a small brick building",
             2: "You are at the top of a hill",
             3: "You are inside a building, a well house for a small stream",
             4: "You are in a valley beside a stream",
             5: "You are in the forest",
             6: "You are standing in from of a Castle",
             7: "You are in the Castle Gardens",
             8: "You have entered the Castle Kitchen",
             9: "You have entered the Castle Foyer"}

 

exits = {0: {"Q": 0},
         1: {"W": 2, "E": 3, "N": 5, "S": 4, "Q": 0},
         2: {"N": 5, "Q": 0},
         3: {"W": 1, "Q": 0, "item": "Castle Key"},
         4: {"N": 1, "W": 2, "Q": 0},
         5: {"W": 2, "S": 1, "Q": 0, "item": "Blade"},
         6: {"N": 7, "S": 5},
         7: {"S": 6, "E": 8},
         8: {"W": 7},
         9: {"W": 8}}


 

vocabulary = { "QUIT":  "Q",
               "NORTH": "N",
               "SOUTH": "S",
               "EAST":  "E",
               "WEST":  "W",
               "INVENTORY": "I"}

 

def move_direction():
        global c_used
        c_used = False
        global opens
        opens = False
        loc = 1
        while True:
            availableExits = ", ".join(exits[loc].keys())
            print(locations[loc])

            if loc == 0:
                print("GAME OVER!")
                choose = input("Type 'r' to play again, or 'x' to exit: ").lower()
                if choose == "r":
                    move_direction()
                elif choose == 'x':
                    sys.exit()
                else:
                    print("Wrong input - ending game...")
                    break
 

            if loc == 7:
                c_used = True

            if loc == 8 and not opens:
                code_input = input("What is the passcode? ")
                if code_input == '1234':
                    exits[8]['E'] = 9
                    availableExits = ", ".join(exits[loc].keys())
                    print(colored("Passcode successful... Opening the door.", "green"))
                    opens = True
                elif code_input != '1234' and not opens:
                    print(colored("You need to passcode to unlock the next room", "red"))
                else:
                    pass



 

            if loc == 6 and "Castle Key" not in inventory:
                exits[6]['N'] = 6
                availableExits = ", ".join(exits[loc].keys())
                print(colored("You see a Castle door, but are unable to open it. Seems it requires a key...", "red"))
            elif loc == 6 and "Castle Key" in inventory and c_used is False:
                exits[6]['N'] = 7
                availableExits = ", ".join(exits[loc].keys())
                print(colored("You used to key to unlock the Castle Gardens door.", "green"))                      
 

            direction = input("Available exits are --- " + availableExits + " "+": ").upper()
            print()
            # Parse the user input, using our vocabulary dictionary if necessary
            if len(direction) > 1:   # more than one letter, so check vocab
                words = direction.split()
                for word in words:
                    if word in vocabulary:
                        direction = vocabulary[word]
                        break

 

            if direction in exits[loc]:
                loc = exits[loc][direction]
                print()
                if 'item' in exits[loc]:
                    print(colored(f"You found a {exits[loc]['item']}!\nAdded item to your inventory...", "yellow"))
                    inventory.append(exits[loc]["item"])
                    del exits[loc]['item']
                    # print(exits)
                    # print(inventory)
                    hidden_exits = {5: {"N": 6, "W": 2, "S": 1, "Q": 0, "item": "Blade"}}
                    exits.update(hidden_exits)
                    if any(x == "Blade" for x in inventory):
                        hidden_exits = {5: {"N": 6, "W": 2, "S": 1, "Q": 0}}
                        exits.update(hidden_exits)
                else:
                    availableExits = ", ".join(exits[loc].keys())
            elif direction not in exits[loc] and direction == 'i'.upper():
                print("-" * 110)
                print(colored(f"Inventory Contents: {inventory}", 'magenta'))
                print("-" * 110)
            elif direction not in exits[loc] and direction == 'build torch'.upper() and "Blade" in inventory:
                inventory.append("Torch")
            elif direction not in exits[loc] and direction == 'cls'.upper():
                system('cls')
            elif direction not in exits[loc] and direction == 'help'.upper():
                print(colored(commands, "cyan"))
            else:
                print(colored("You cannot go in that direction", "red"))

 

if choose == "yes" or choose == 'y':
    for char in intro:
        sleep(0.010)
        cprint(char, 'grey', attrs=['bold'], end="")
    move_direction()
elif choose == "no" or choose =='n':
    sys.exit()
else:
    choose = input("Start your Journey (y/n)? ").lower()