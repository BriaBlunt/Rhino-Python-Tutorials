import rhinoscriptsyntax as rs
from math import*

def myFunction(object, translation):
    rs.MoveObject(object, translation)
    print("translation successful!")

strObject = rs.GetObject("pick an object from screen", 4)

print(strObject)

#myFunction(strObject, [ 10,0,0] )
#myFunction(strObject, [ 0,10,0] )
