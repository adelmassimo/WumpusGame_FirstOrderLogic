from proposition import *
from RulesList import *

class KnowledgeBase:
    def __init__(self):
        self.clauses = PrintableLit("\n")

    def TELL(self, q):
        self.clauses.append( q )


    def symbolsInClauses(self):
        s = []
        for arg in self.clauses:
            if arg.isSymbol():
                s.append(str(arg))
        return s

    def ASK(self, q: Formula) -> bool:
        return self.backwardChaining(q)

    def printAgend(self):
        print("Agend: ")
        for i in range(0, len(self.agend)):
            print(str(self.agend[i]))

    def printCount(self):
        print("Count: " + str(self.count))


    def printClauses(self):
        print("Clauses: " + str(self.clauses))

    def backwardChaining(self, q :Formula):
        if str(q) in self.clauses.stringList():         # se la formula q è già presente in clauses è ovvio
            return True                                 # che sia vera

        elif isinstance(q, Not):                        # nel caso in cui la formula sia una negazione
            return not self.backwardChaining(q.child)   # ritorno il valore negato del figlio

        elif isinstance(q, And):
            return self.backwardChaining(q.leftOp) and self.backwardChaining(q.rightOp)

        elif isinstance(q, Or):
            return self.backwardChaining(q.leftOp) or self.backwardChaining(q.rightOp)

        for arg in self.clauses:
            if isinstance(arg, Iff):
                if str(arg.leftOp) == str(q):
                    return self.backwardChaining(arg.rightOp)
                elif str(arg.rightOp) == str(q):
                    return self.backwardChaining(arg.leftOp)
            elif isinstance(arg, Implies):
                if str(arg.leftOp) == str(q):
                    return self.backwardChaining(arg.rightOp)
        return False