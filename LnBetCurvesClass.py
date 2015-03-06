import rhinoscriptsyntax as rs


class LnBetCurves:

    def __init__(self, _strCurve1, _strCurve2, _numOfDivs):
        self.strCurve1 = _strCurve1
        self.strCurve2 = _strCurve2
        self.numOfDivs = _numOfDivs

    def drawLineBetweenCurves(self):
        ptList1 = rs.DivideCurve( self.strCurve1, self.numOfDivs, True, True)
        ptList2 = rs.DivideCurve( self.strCurve2, self.numOfDivs, True, True)

        count = 0
        for i in ptList1:
            rs.AddLine( ptList1[count] , ptList2[count]  )
            count += 1

        print ("everything is okay so far")
