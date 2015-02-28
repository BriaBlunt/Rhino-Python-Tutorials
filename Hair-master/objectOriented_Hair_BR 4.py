import rhinoscriptsyntax as rs
#import myDefinitions as defs
import random as r
run=True
a = []

def GeneratePointFromCurve(inputCrv,distance,angle,threshold):
    #generates a point off of a curve of a line
    #returns list: [ point , vector ] 
    crvDomain = rs.CurveDomain(inputCrv)
    ptParam = ((crvDomain[1]-crvDomain[0])/2)+crvDomain[0]
    crvPt = rs.EvaluateCurve(inputCrv,ptParam)
    curveTan = rs.CurveTangent(inputCrv,ptParam)
    cPlane = rs.PlaneFromNormal(crvPt,curveTan)
    rotVec = rs.VectorRotate(curveTan,r.uniform(angle-threshold,angle+threshold),cPlane[1])
    newVec = rs.VectorRotate(rotVec,r.uniform(0,360),curveTan)
    newVec = rs.VectorUnitize(newVec)
    tailVec = rs.VectorScale(newVec,tailDist)
    baseVec = rs.VectorScale(newVec,distance)
    headVec = rs.VectorScale(newVec,headDist)
    newPt = rs.PointAdd(crvPt,baseVec)

    newBranch = Branch(crvPt,baseVec,[newPt,headVec],[crvPt,rs.VectorReverse(tailVec)])
    objList.append(newBranch)
    return [newPt,baseVec]
def GeneratePointFromPoint(inputPt,prevVec,distance,angle,threshold):
    cPlane = rs.PlaneFromNormal(inputPt,prevVec)
    rotVec = rs.VectorRotate(prevVec,r.uniform(angle-threshold,angle+threshold),cPlane[1])
    newVec = rs.VectorRotate(rotVec,r.uniform(0,360),prevVec)
    newVec = rs.VectorUnitize(newVec)
    tailVec = rs.VectorScale(newVec,tailDist)
    baseVec = rs.VectorScale(newVec,distance)
    headVec = rs.VectorScale(newVec,headDist)
    newPt = rs.PointAdd(inputPt,baseVec)
    newBranch = Branch(inputPt,baseVec,[newPt,headVec],[inputPt,rs.VectorReverse(tailVec)])
    objList.append(newBranch)
    return [newPt,baseVec]
class Branch():


    def __init__(self, BASE,VECTOR, HEAD, TAIL):
        self.base = BASE
        #vector list: previous vector,currentvector
        self.vec = VECTOR
        #self.bounds = BOUNDS
        #self.bPts = BRANCHPOINTS
        self.head = HEAD
        self.tail = TAIL
        #self.gen = GEN
        
    def grow(self):

        p1 = rs.PointAdd(self.head[0],self.head[1])

        p2 = rs.PointAdd(self.tail[0],self.tail[1])
        rs.AddLine(p1,p2)
#create the Branching
def update():
    for i in range (0, len(objList)):
        objList[i].grow()

#def generateHair():
    
def addCurve (inputCrv, distMin, distMax,inflow, arrVolume, gens, maxGen,vecInfluence):
    #rs.EnableRedraw(False)
    newgens = gens+1
    
    if gens<maxGen:
        
        domain = rs.CurveDomain (inputCrv)
        randP1 = r.uniform(domain[0],domain[1])
        curvePoint = rs.EvaluateCurve(inputCrv, randP1)
        
        if curvePoint != None:
            
    #Curve point Tangent Vector
            strNewCrv = generate(inputCrv,curvePoint,randP1,distMin,distMax,rotAngle,angleThresh,vecInfluence)
            strNewCrv = collideTest(strNewCrv,arrVolume)
            lineList.append(strNewCrv)
            rSd = r.randint(1, 10)
            if rSd> 1 :
                vecInf1 = influencer(strNewCrv,lineList,VInfScale)
                vecInf2 = pathInfluence(strNewCrv,inflow,curvePullDistance)
                vecInfTotal = vectorAverage([vecInf1,vecInf2])
                addCurve (strNewCrv, distMin, distMax, inflow, arrVolume, newgens, maxGen, vecInfTotal)
            if rSd>4:
                vecInf1 = influencer(strNewCrv,lineList,VInfScale)
                vecInf2 = pathInfluence(strNewCrv,inflow,curvePullDistance)
                vecInfTotal = vectorAverage([vecInf1,vecInf2])
                addCurve (strNewCrv, distMin, distMax, inflow, arrVolume, newgens, maxGen, vecInfTotal)
    rs.EnableRedraw(True)

def main():
    startCrv = rs.GetObject("select start Curve",4)
    if startCrv is None:
        print "curve Fail"
        return 
    copyCrv = rs.CopyObject(startCrv)
    divPts = rs.DivideCurve(startCrv,divCount)
    paramList = []
    for i in range (0,len(divPts)):
        cP = rs.CurveClosestPoint(startCrv,divPts[i])
        paramList.append(cP)
    divCrv = rs.SplitCurve(startCrv,paramList)
    
    for i in range (0,len(divCrv)):
        branchPt = GeneratePointFromCurve(divCrv[i],dist,rotAngle,angThreshold)
        #rs.AddLine(rs.CurveMidPoint(divCrv[i]),branchPt[0])
        
        treeLoop(0,maxBranch,branchPt,angThreshold)
        rs.DeleteObject(divCrv[i])
def treeLoop(currentGen,maxGen,prevPt,angThreshold):
    if currentGen < maxGen:
        newPt = GeneratePointFromPoint(prevPt[0],prevPt[1],dist,rotAngle,angThreshold)
        #rs.AddLine(prevPt[0],newPt[0])
        treeLoop(currentGen+1,maxGen,newPt,angThreshold)
    else:
        return
            
objList = []

rotAngle = 19
angThreshold = 5
divCount = 1
maxBranch = 12
dist = 10
tailDist = 0

headDist = 4

#


if run:
    main()
    update()

