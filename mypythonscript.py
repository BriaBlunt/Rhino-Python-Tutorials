import rhinoscriptsyntax as rs
from math import*

#for i in range(0,100):
    #rs.AddPoint( [sin(i),i,0] )


i = 0
while i < 100:
    rs.AddPoint( [sin(i),i,0] )
    i += 1
