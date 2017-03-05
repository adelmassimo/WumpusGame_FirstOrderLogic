from RulesList import *

class Formula:
    def __NOT__(self):
        return Not(self)

    def __AND__(self, other):
        return And(self, other)

    def __OR__(self, other):
        return  Or(self, other)

    def __IFF__(self, other):
        return Iff(self, other)

    def __IMPLIES__(self, other):
        return Implies(self, other )

    def value(self, q):
        raise NotImplementedError("Formula non può essere valutata")

    def countSymbols(self):
        raise NotImplementedError("Non implementato")

    def contain(self, item):
        raise NotImplementedError("Non implementato")

    def getSymbols(self):
        raise NotImplementedError("Non implementato")

    def isSymbol(self):
        if isinstance(self, Atomic): return True
        if isinstance(self, Not):
            return self.child.isSymbol()
        return False

    def toCNF(self):
        q = self

        q = self.eliminate_implications(q)

        q = self.move_not_inwards(q)

        q = self.distribute_and_over_or(q)

        return q


    def eliminate_implications(self, s):
        if not isinstance(s, Atomic) and not isinstance(s, Not):
            s.leftOp = self.eliminate_implications(s.leftOp)
            s.rightOp = self.eliminate_implications(s.rightOp)
        if isinstance(s, Implies):
            a = s.leftOp
            b = s.rightOp
            return a.__NOT__().__OR__(b)
        elif isinstance(s, Iff):
            a = s.leftOp
            b = s.rightOp
            return a.__OR__(b.__NOT__()).__AND__(b.__OR__(a.__NOT__()))


        return s

    def move_not_inwards(self, s):
        if isinstance(s, Not):
            a = s.child
            if isinstance(a, Not):
                return self.move_not_inwards(a.child)  # ~~A ==> A
            if isinstance(a, And):
                x = a.leftOp.__NOT__().__OR__(a.rightOp.__NOT__())
                x.leftOp = self.move_not_inwards(x.leftOp)
                x.rightOp = self.move_not_inwards(x.rightOp)
                return x
            if isinstance(a, Or):
                x = a.leftOp.__NOT__().__AND__(a.rightOp.__NOT__())
                x.leftOp = self.move_not_inwards(x.leftOp)
                x.rightOp = self.move_not_inwards(x.rightOp)
                return x
            return s
        else:
            return s

    def distribute_and_over_or(self, s):
        if not isinstance(s, Atomic) and not isinstance(s, Not):
            s.leftOp = self.distribute_and_over_or(s.leftOp)
            s.rightOp = self.distribute_and_over_or(s.rightOp)

        if isinstance(s, Or):
            if isinstance(s.rightOp, And):
                s = s.leftOp.__OR__(s.rightOp.leftOp).__AND__(s.leftOp.__OR__(s.rightOp.rightOp))
            if isinstance(s.leftOp, And):
                s = s.rightOp.__OR__(s.leftOp.rightOp).__AND__(s.rightOp.__OR__(s.leftOp.leftOp))

        return s


class BinaryOperator(Formula):
    op = ""
    def __init__(self, left: Formula, right: Formula):
        self.leftOp = left
        self.rightOp = right

    def __str__(self):
        return "( " + str(self.leftOp) + self.op + str(self.rightOp) + " )"

    def contain(self, item):
        if str(self) == str(item):
            return True
        return self.leftOp.contain(item) or self.rightOp.contain(item)

    def getSymbols(self):
        result = PrintableLit(" - ")
        l = self.leftOp.getSymbols()
        r = self.rightOp.getSymbols()

        for i in l:
            if not str(i) in result:
                result.append(str(i))
        for i in r:
            if not str(i) in result:
                result.append(str(i))

        return result

    def countSymbols(self):
        return self.leftOp.countSymbols() + self.rightOp.countSymbols()


class And(BinaryOperator):
    op = " ∧ "

    def value(self, q):
        return self.leftOp.value(q) and self.rightOp.value(q)



class Or(BinaryOperator):
    op = " ∨ "

    def value(self, q):
        return self.leftOp.value(q) or self.rightOp.value(q)



class Implies(BinaryOperator):
    op = " → "

    def value(self, q):
        return not self.leftOp.value(q) or self.rightOp.value(q)


class Iff(BinaryOperator):
    op =" ↔ "

    def value(self, q):
        return self.leftOp.value(q) is self.rightOp.value(q)


class Not(Formula):
    def __init__(self, other: Formula):
        self.child = other

    def value(self, q):
        return not self.child.value(q)

    def __str__(self):
        return "¬" + str(self.child)

    def contain(self, item):
        if str(self) == str(item):
            return True
        return self.child.contain(item)

    def getSymbols(self):
        if self.isSymbol():
            return [self]
        return self.child.getSymbols()

    def countSymbols(self):
        return self.child.countSymbols()



class Atomic(Formula):
    def __init__(self, name: str):
        self.name = name

    def value(self, q):
        return str(self) in q or "¬¬"+str(self) in q

    def __str__(self):
        return self.name

    def contain(self, item):
        if str(self) == str(item):
            return True
        return False

    def getSymbols(self):
        return [self]

    def countSymbols(self):
        return 1

def possibleWorlds(q :Formula):

    if q.isSymbol():                #setup iniziale
        return [str(q.toCNF())]
    countWumpus = 0
    countPits = 0
    base = q.getSymbols()
    result = PrintableLit("\n")

    for i in range(0, pow(2,len(base))):    #avrò 2^n possibili mondi, n = numero di simboli
        x = str(bin(i))[2:]                 #utilizzo una variabile binaria d'appoggio per tenere conto della combinazione
        while len(x) < len(base):           # "normalizzp la lunghezza di tutte le stringhe: le prime sono più corte
            x = "0" + x
        tmp = PrintableLit(" ")
        for j in range(0, len(x)):
            if x[j] == "0":
                tmp.append( "¬"+str(base[j]) )
            else:
                tmp.append( str(base[j]) )
                if "W" in str(base[j]) and not "¬" in str(base[j]):
                    countWumpus += 1
                if "P" in str(base[j]) and not "¬" in str(base[j]):
                    countPits += 1
        if countWumpus <= 1 and countPits <= 3:
            if q.value(tmp):
                result.append(tmp)
        countWumpus = 0
        countPits = 0
    return result

def getWumpusPositionFromPW(pWorld :list):
    for arg in pWorld:
        if "W" in arg and not "¬" in arg:
            return int(arg[1]), int(arg[2])

def getPitPositionFromPW(pWorld :list):
    result = []
    for arg in pWorld:
        if "P" in arg and not "¬" in arg:
            result.append( (int(arg[1]), int(arg[2])) )
    return result

def fitWorld(pWorld: list, dim = 3):
    for i in range(0,dim):
        for j in range(0,dim):
            if "¬W"+str(i)+str(j) in pWorld and "¬P"+str(i)+str(j) in pWorld:
                pWorld.remove("¬W"+str(i)+str(j))
                pWorld.remove("¬P"+str(i)+str(j))
                pWorld.append("OK"+str(i)+str(j))

