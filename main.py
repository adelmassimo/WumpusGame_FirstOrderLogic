from proposition import *
from agent import *

a = Atomic("A")
b = Atomic("B")
c = Atomic("C")
d = Atomic("D")
e = Atomic("E")
f = Atomic("F")
g = Atomic("G")

KB = KnowledgeBase()

p1 = a.__AND__(b).__AND__(c)
tot = d.__IFF__(p1)

a, b = 0,0

W = World(4)
W.printMap()
agent = Agent(KB, W, W.environmentRules())
result = agent.play()




#agent.kb.printClauses()