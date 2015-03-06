import rhinoscriptsyntax as rs
from math import*

class myClass:

    def __init__(self, _name):
        self.name = _name

    def printName(self):
        print(self.name)

    def printAlert(self):
        print("Alert!")

obj1 = myClass("Ana")
obj1.printName()

obj2 = myClass("Joe")
obj2.printName()
