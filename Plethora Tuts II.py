import rhinoscriptsyntax as rs
from LnBetCurvesClass import*

strC1 = rs.GetObject("pick first curve", 4)
strC2 = rs.GetObject("pick second curve", 4)

obj01 = LnBetCurves (strC1, strC2, 60)
obj01.drawLineBetweenCurves()
