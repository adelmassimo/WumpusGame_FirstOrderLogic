from knowledgeBase import *
from RulesList import *
import random

class Room:
    def __init__(self, x, y):
        self.rules = PrintableLit(" ")
        self.x = x
        self.y = y

    def setRules(self, q: Formula):
        self.rules.append(q)

    def getRules(self):
        return self.rules

    def __str__(self):
            return str(self.rules)

class World:                       #wumpus = w     agent = a   pit = p    brew = b    smell = s
    def __init__(self, dim = 4):
        self.map = []
        self.dim = dim
        for i in range(0, dim):
            self.map.append(list())
        for i in range(0, dim):
            for j in range(0, dim):
                self.map[i].append(Room(i,j))
        self.setWorld()

    def printMap(self):
        string = "| "
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                string += str(self.map[i][j]) + " | "
            string += "\n| "
        print( string )

    def setWorld(self):
        self.setWumpus()
        for i in range(0, 3):
            self.setPit()
        self.setGold()
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                suffix = str(i)+str(j)
                if not "W"+suffix in str(self.map[i][j].getRules()):
                    self.map[i][j].setRules(Atomic("W"+suffix).__NOT__())
                if not "P" + suffix in str(self.map[i][j].getRules()):
                    self.map[i][j].setRules(Atomic("P" + suffix).__NOT__())

    def setWumpus(self):
        wx = random.randrange(0, self.dim)
        wy = random.randrange(0, self.dim)
        if wx == wy == 0:
            self.setWumpus()
        self.map[wx][wy].setRules(Atomic("W" + str(wx) + str(wy)))
        wy -= 1
        if wy in range(0, self.dim):
            if not ("P" in self.map[wx][wy].getRules() and not "¬P" in self.map[wx][wy].getRules()):
                self.map[wx][wy].setRules(Atomic("S" + str(wx) + str(wy)))
        wy += 2
        if wy in range(0, self.dim):
            if not ("P" in self.map[wx][wy].getRules() and not "¬P" in self.map[wx][wy].getRules()):
                self.map[wx][wy].setRules(Atomic("S" + str(wx) + str(wy)))
        wy -= 1
        wx -= 1
        if wx in range(0, self.dim):
            if not ("P" in self.map[wx][wy].getRules() and not "¬P" in self.map[wx][wy].getRules()):
                self.map[wx][wy].setRules(Atomic("S" + str(wx) + str(wy)))
        wx += 2
        if wx in range(0, self.dim):
            if not ("P" in self.map[wx][wy].getRules() and not "¬P" in self.map[wx][wy].getRules()):
                self.map[wx][wy].setRules(Atomic("S" + str(wx) + str(wy)))

    def setGold(self):
        wx = random.randrange(0, self.dim)
        wy = random.randrange(0, self.dim)
        if wx == wy == 0 or ("P"+str(wx)+str(wy) in str(self.map[wx][wy].getRules())) or ("W"+str(wx)+str(wy) in str(self.map[wx][wy].getRules())) :
            self.setGold()
        else:
            self.map[wx][wy].setRules(Atomic("G" + str(wx) + str(wy)))


    def setPit(self):
        wx = random.randrange(0, self.dim)
        wy = random.randrange(0, self.dim)
        if wx == wy == 0 or "P" == str(self.map[wx][wy])[0]:
            self.setPit()
        self.map[wx][wy].setRules(Atomic("P" + str(wx) + str(wy)))
        wy -= 1
        if wy in range(0, self.dim):
            if not ("P" in self.map[wx][wy].getRules() and not "¬P" in self.map[wx][wy].getRules() and "W" in self.map[wx][wy].getRules() and "¬W" in self.map[wx][wy].getRules() ):
                self.map[wx][wy].setRules(Atomic("B" + str(wx) + str(wy)))
        wy += 2
        if wy in range(0, self.dim):
            if not ("P" in self.map[wx][wy].getRules() and not "¬P" in self.map[wx][wy].getRules() and "W" in self.map[wx][wy].getRules() and "¬W" in self.map[wx][wy].getRules() ):
                self.map[wx][wy].setRules(Atomic("B" + str(wx) + str(wy)))
        wy -= 1
        wx -= 1
        if wx in range(0, self.dim):
            if not ("P" in self.map[wx][wy].getRules() and not "¬P" in self.map[wx][wy].getRules() and "W" in self.map[wx][wy].getRules() and "¬W" in self.map[wx][wy].getRules() ):
                self.map[wx][wy].setRules(Atomic("B" + str(wx) + str(wy)))
        wx += 2
        if wx in range(0, self.dim):
            if not ("P" in self.map[wx][wy].getRules() and not "¬P" in self.map[wx][wy].getRules() and "W" in self.map[wx][wy].getRules() and "¬W" in self.map[wx][wy].getRules() ):
                self.map[wx][wy].setRules(Atomic("B" + str(wx) + str(wy)))

    def environmentRules(self):
        rulesList = []
        dim = self.dim

        for i in range(0, dim):
            for j in range(0, dim):
                right = Atomic("P" + str(i) + str(j))
                left = None
                if i - 1 in range(0, dim):
                    left = Atomic("B" + str(i - 1) + str(j))
                if i + 1 in range(0, dim):
                    if left != None:
                        left = left.__OR__(Atomic("B" + str(i + 1) + str(j)))
                    else:
                        left = Atomic("B" + str(i + 1) + str(j))
                if j - 1 in range(0, dim):
                    left = left.__OR__(Atomic("B" + str(i) + str(j - 1)))
                if j + 1 in range(0, dim):
                    left = left.__OR__(Atomic("B" + str(i) + str(j + 1)))
                rulesList.append(left.__IFF__(right))

        for i in range(0, dim):
            for j in range(0, dim):
                right = Atomic("W" + str(i) + str(j))
                left = None
                if i - 1 in range(0, dim):
                    left = Atomic("S" + str(i-1) + str(j))
                if i + 1 in range(0, dim):
                    if left != None:
                        left = left.__OR__(Atomic("S" + str(i + 1) + str(j)))
                    else:
                        left = Atomic("S" + str(i + 1) + str(j))
                if j - 1 in range(0, dim):
                    left = left.__OR__(Atomic("S" + str(i) + str(j - 1)))
                if j + 1 in range(0, dim):
                    left = left.__OR__(Atomic("S" + str(i) + str(j + 1)))
                rulesList.append(left.__IFF__(right))
        # POTREI ACCORPARE I DUE FOR USANDO l1, l2, r1 r2 ... QUANDO HO TEMPO. SE, COME NO
        return rulesList


