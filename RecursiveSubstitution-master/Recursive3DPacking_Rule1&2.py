import rhinoscriptsyntax as rs
import math as m
import random as r



def Main():
    
    gens = rs.GetReal("how many Gens?", 4)
    if gens is None: #error Checking
        print "forgot input"
        return
    
    startingArr = rs.GetObjects("select starting shapes", 16)
    if gens is None: #error Checking
        print "forgot input"
        return
    
    shapeOneNumber = 18
    shapeTwoNumber = 6
    
    objArr1 = []
    objArr2 = []
    
    for i in range(0,shapeOneNumber):
        arrTemp = rs.ObjectsByName("T"+str(i))
        if arrTemp is None:
            print "missing parts"
            return
        objArr1.append(arrTemp[0])
        
    for i in range(0,shapeTwoNumber):
        arrTemp = rs.ObjectsByName("TO"+str(i))
        if not arrTemp:
            print "missing parts"
            return
        objArr2.append(arrTemp[0])
    rs.EnableRedraw(False)
    
    for shapeRun in startingArr:
        blnObj = True
        
        if r.random() > .5:
            blnObj = True
        
        if blnObj:
            ThreeDPack(shapeRun, objArr1, gens, gens, objArr1, objArr2)
            rs.DeleteObject(shapeRun)
        else:
            ThreeDPack(shapeRun, objArr2, gens, gens, objArr1, objArr2)
            rs.DeleteObject(shapeRun)
                
    
    rs.EnableRedraw(True)

def ThreeDPack(target, objArr, gens, maxGen, objArr1, objArr2):
    
    if gens>0:
        
        arrBaseExplodedSrfs = rs.ExplodePolysurfaces(objArr[0], False)
        basePts = rs.SurfacePoints(arrBaseExplodedSrfs[1])
        base3Pts = [basePts[0], basePts[1], basePts[2]]
        rs.DeleteObjects (arrBaseExplodedSrfs)
        # targetObject
        
        arrTargetExplodedSrfs = rs.ExplodePolysurfaces(target, False)
        targetPts = rs.SurfacePoints(arrTargetExplodedSrfs[1])
        target3Pts = [targetPts[0], targetPts[1], targetPts[2]]
        rs.DeleteObjects (arrTargetExplodedSrfs)
        
        # orient objects 3pts no scale
        newObjs = OrientMultObjects(objArr, base3Pts, target3Pts, 1)
        rs.ObjectName (newObjs, "0")
        #calculate a scale amount based on meta objects and new objects
        scale = (1 / rs.Distance(basePts[0], basePts[1])) * rs.Distance(targetPts[0], targetPts[1])
        #scale objects
        rs.ScaleObjects (newObjs, targetPts[0], [scale, scale, scale] )
        
        
        
        for i in range(0,len(newObjs)):
            blnObjOne = True
            if r.random() > .5:
                blnObjOne = False
            
            if r.random() > .5:
                
                if blnObjOne:
                    
                    ThreeDPack(newObjs[i], objArr1, gens-1, maxGen, objArr1, objArr2)
                    rs.DeleteObject(newObjs[i])
                else:
                    ThreeDPack(newObjs[i], objArr2, gens-1, maxGen, objArr1, objArr2)
                    rs.DeleteObject(newObjs[i])


def OrientMultObjects(obj, ref, tar,flag):
    
    newObj= []
    
    for i in range(0,len(obj)):
        
        newObj.append(rs.OrientObject(obj[i],ref,tar,flag))
        
    return newObj

if( __name__ == "__main__" ):
    Main()




