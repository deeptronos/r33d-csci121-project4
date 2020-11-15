from room import Room
from player import Player
from item import Item
from monster import Monster
from gametime import GameTime
import os
import updater

player = Player()
gT = GameTime()

def createWorld():

    #House Rooms:
    br = Room("Your Bedroom")
    lr = Room("Your Living Room")
    #bY = Room("Your Backyard. It contains a modest g is 6x2 feet large. ")
    bY = Room("Your Backyard")
    #External Rooms:
    outside         = Room("Outside")   #   Generic 'outside' location, to tie together all of the colony's accessable location
    farmersMarket   = Room("The farmer's market")
    gardenSupply    = Room("'Gardener's Delight' Garden Supply Emporium")
    fieldOffice     = Room("Wasteland Field Office")


    Room.connectRooms(br, "living room",  lr, "bedroom")
    Room.connectRooms(lr, "backyard", bY, "living room")
    Room.connectRooms(lr, "outside", outside, "inside")

    Room.connectRooms(outside, "farmers market", farmersMarket, "home")
    Room.connectRooms(outside, "garden supply", gardenSupply, "home")
    Room.connectRooms(outside, "field office", fieldOffice, "home")

    i = Item("Macbook", "This is your 3019 16-Inch Macbook Vro.")
    i.putInRoom(br)
    # Room.connectRooms(a, "east", b, "west")
    # Room.connectRooms(c, "east", d, "west")
    # Room.connectRooms(a, "north", c, "south")
    # Room.connectRooms(b, "north", d, "south")
    #i = Item("Rock", "This is just a rock.")
    #i.putInRoom(b)
    player.location = br
    #Monster("Bob the monster", 20, b)

def header():
    title = "Anno Domini 3049: Newcomer Gardening Exhibition (Radiation Hell Fantasy)"
    date = gT.formattedDate()
    wDim = os.get_terminal_size()[0]

    iterant = 0
    line1, line2, line3, output = "", "", "", ""
    for i in range(wDim):   #   For loop to make a line of text the width of the terminal with the title centered in the middle
        if i < (wDim // 2) - (len(title)//2) or i >= (wDim // 2) + (len(title)//2):
            line1 += " "
        elif i >= (wDim // 2) - (len(title)//2):
            line1 += title[i - (wDim // 2) - (len(title)//2)]

    for i in range(wDim):   #   For loop that makes a line of text with the date, then fills to the window width with a symbol
        if (i) < len(date) + 2 and i > 1:
            line2 += date[i - 2]
        elif i > len(date) + 2:
            line2 += "𖡻"
        else:
            line2 += " "

    for i in range(wDim):   #   For loop that fills a string to window width with a symbol
        line3 += "𝍅"

    for i in range(3):  #   Puts all these different strings into one, separating them by new lines
        if i == 0:
            output += line1
        elif i == 1:
            output += line2
        elif i == 2:
            output += line3
        output += "\n"

    return output

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def printSituation():
    clear()
    print(header())

    print(player.location.desc)
    print()
    if player.location.hasMonsters():
        print("This room contains the following monsters:")
        for m in player.location.monsters:
            print(m.name)
        print()
    if player.location.hasItems():
        print("This room contains the following items:")
        for i in player.location.items:
            print(i.name)
        print()
    print("You can go to the following locations:")
    for e in player.location.exitNames():
        print(e)
    print()

def showHelp():
    clear()
    print("go <direction> -- moves you in the given direction")
    print("inventory -- opens your inventory")
    print("pickup <item> -- picks up the item")
    print()
    input("Press enter to continue...")

def showPlayerStats():
    clear()
    print("Let's take a look at you:")
    print(visualizeContainer(26, "down"))
    for i in player.attributes: #   For each string in the list player.attributes...
        player.displayStat(i)   #   Display that stat
    print(visualizeContainer(26, "up"))
    input("Press enter to continue...")

def visualizeContainer(width, direction):
    output = ""
    charList = ["╶", "╴", "╭","╮","╰","╯","━", "─"]
    for i in range(width):
        if i == 0:
            if direction == "up":
                output += charList[4]
            elif direction == "down":
                output += charList[2]
        elif i == width - 1:
            if direction == "up":
                output += charList[5]
            elif direction == "down":
                output += charList[3]
        else:
            output += charList[7]
    return output

createWorld()
playing = True
while playing and player.alive:
    printSituation()
    commandSuccess = False
    timePasses = False
    while not commandSuccess:
        commandSuccess = True
        command = input("What now? ")
        commandWords = command.split()

        if commandWords[0].lower() == "go":   #CAN handle multi-word directions now that we're using goDirection on the sliced input string
            player.goDirection(command[3:])
            timePasses = True

        elif commandWords[0].lower() == "pickup":  #can handle multi-word objects
            targetName = command[7:]
            target = player.location.getItemByName(targetName)
            if target != False:
                player.pickup(target)
            else:
                print("No such item.")
                commandSuccess = False

        elif commandWords[0].lower() == "drop":
            targetName = command[5:]
            target = player.getInventoryItemByName(targetName)
            if target != False: #   If getInventoryItemByName doesn't return false...
                player.drop(target)
            else:
                print("No such item.")
                commandSuccess = False

        elif commandWords[0].lower() == "inspect":
            targetName = command[8:]
            player.inspectItem(targetName)
            #print("target: ", target)

        elif commandWords[0].lower() == "me":
            showPlayerStats()
        elif commandWords[0].lower() == "inventory":
            player.showInventory()
        elif commandWords[0].lower() == "help":
            showHelp()
        elif commandWords[0].lower() == "exit":
            playing = False
        elif commandWords[0].lower() == "attack":
            targetName = command[7:]
            target = player.location.getMonsterByName(targetName)
            if target != False:
                player.attackMonster(target)
            else:
                print("No such monster.")
                commandSuccess = False
        else:
            print("Not a valid command")
            commandSuccess = False
    if timePasses == True:
        updater.updateAll()
