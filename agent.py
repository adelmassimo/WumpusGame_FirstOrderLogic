from wumpusWorld import *

class Agent:
    def __init__(self, KB: KnowledgeBase, W: World, initialSet=None):
        self.x = 0
        self.y = 0
        self.kb = KB
        self.world = W
        self.brews, self.discovered, self.frontier, self.safe = [], [], [], []
        self.alive, self.win = True, False
        for axiom in initialSet:
            self.kb.TELL( axiom )

    def percept(self):
        for fact in self.world.map[self.x][self.y].getRules():
            if str(fact) not in self.kb.clauses:
                self.kb.TELL( fact )
                if str(fact)[0] == "B":
                    self.brews.append(fact)
                if str(fact)[0] == "W" or str(fact)[0] == "P":
                    self.alive = False
                elif str(fact)[0] == "G":
                    self.win = True

    def play(self):
        randChoises = 0
        self.moveTo(0,0)
        while self.alive and not self.win:
            self.percept()
            self.setSafeRooms()
            if self.safe != []:
                self.moveTo( self.safe[0][0], self.safe[0][1])
            else:
                if len(self.frontier) == 0:
                    alive = False
                else:
                    randChoises = randChoises+1
                    choice = random.randrange(0, len(self.frontier))
                    self.moveTo( self.frontier[choice][0], self.frontier[choice][1])
        if self.win:
            print("WON")
            return (True, randChoises+1)
        else:
            print("LOSE")
            return (False, randChoises+1)

    def setSafeRooms(self):
        self.safe.clear()
        for room in self.frontier:
            P, W = "P"+str(room[0])+str(room[1]), "W"+str(room[0])+str(room[1])
            if self.kb.ASK( Atomic(P).__NOT__() ) and self.kb.ASK( Atomic(W).__NOT__() ):
                self.safe.append( room )

    def buildFrontier(self):
        self.frontier.clear()
        for room in self.discovered:
            x,y = room[0],room[1]

            if not (x+1, y) in self.discovered and x+1 < self.world.dim and not (x+1, y) in self.frontier:
                self.frontier.append((x+1,y))
            if not (x-1, y) in self.discovered and x-1 >= 0 and not (x-1, y) in self.frontier:
                self.frontier.append((x-1,y))
            if not (x, y+1) in self.discovered and y+1 < self.world.dim and not (x, y+1) in self.frontier:
                self.frontier.append((x,y+1))
            if not (x, y-1) in self.discovered and y-1 >= 0 and not (x, y-1) in self.frontier:
                self.frontier.append((x,y-1))

    def moveTo(self, i ,j):
        print("agent in: "+str(i)+str(j))
        self.x = i
        self.y = j
        self.percept()
        self.discovered.append( (i, j) )
        self.buildFrontier()

    def probabilisticReasoning(self):
        if self.brews ==[]:
            return

        probs = []
        tot = self.brews[0]

        for i in range(1, len(self.brews)):
            tot.__AND__(self.brews[i])

        for room in self.frontier:
            x = Atomic("P"+str(room[0])+str(room[1]))
            w = tot.__AND__(x)
            result = possibleWorlds(w)
            p = 1.0
            print(result)
            for world in result:
                for arg in world:
                    if arg != str(x) and arg[0] == "P":
                        p = p * 0.2
                    elif arg != str(x) and "¬P" in arg:
                        p = p * 0.8
            probs.append(p)
        print(probs)

