import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.location = None
        self.items = []
        self.health = 50
        self.alive = True
        self.attributes = ["self.health"]     #   For use in displaying current status ("me" command)
    def goDirection(self, direction):
        self.location = self.location.getDestination(direction)
    def pickup(self, item):
        self.items.append(item)
        item.loc = self
        self.location.removeItem(item)

    def drop(self, item):
        print("item: ", item)
        print("self.items: ", self.items)
        self.items.remove(item)
        item.loc = self.location
        self.location.addItem(item)

    def displayStat(self, statName):    #   Function code concept credit to https://stackoverflow.com/a/32001042
        print(statName, '=', repr(eval(statName)))

    def getInventoryItemByName(self, name): #   Get item in inventory by name
        for i in self.items:
            if i.name.lower() == name.lower():
                return i

        return False

    def showInventory(self):
        clear()
        print("You are currently carrying:")
        print()
        for i in self.items:
            print(i.name)
        print()
        input("Press enter to continue...")
    def attackMonster(self, mon):
        clear()
        print("You are attacking " + mon.name)
        print()
        print("Your health is " + str(self.health) + ".")
        print(mon.name + "'s health is " + str(mon.health) + ".")
        print()
        if self.health > mon.health:
            self.health -= mon.health
            print("You win. Your health is now " + str(self.health) + ".")
            mon.die()
        else:
            print("You lose.")
            self.alive = False
        print()
        input("Press enter to continue...")
