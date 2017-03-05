
class PrintableLit(list):
    def __init__(self, spacer = " "):
        self.spacer = spacer

    def __str__(self):
        s = ""
        for arg in self:
            if str(arg)[0] != "¬":
                s += str(arg) + self.spacer
        if s == "":
            s = "-"
        return s

    def stringList(self):
        result = []
        for arg in self:
            result.append( str(arg) )
        return result