import rhinoscriptsyntax as rs
import math as m
import random as r



def addCurve (inputCrv, distMin, distMax, arrVolume, gens, maxGen):
    
    newgens = gens+1
    
    if gens<maxGen:
        
        domain = rs.CurveDomain (inputCrv)
        
        randP1 = r.uniform(domain[0],domain[1])
        
        curvePoint = rs.EvaluateCurve(inputCrv, randP1)
        
        if not curvePoint is None:
            
            rVecX = r.uniform(-1,1)
            rVecY = r.uniform(-1,1)
            rVecZ = r.uniform(-1,1)
            
            #rs.Prompt (rVecX)
            
            
            rScaleFactor = r.uniform(distMin,distMax )
            
            randVector = rs.VectorCreate([0,0,0],[rVecX,rVecY,rVecZ] )
            
            randVector=rs.VectorScale (randVector,rScaleFactor)
            
            arrNewPt = rs.VectorAdd(curvePoint, randVector)
            
            
            strNewCrv = rs.AddLine(curvePoint, arrNewPt)
            
            
            rScale = r.uniform(1.2,2.5)
            
            cMid = rs.CurveMidPoint(strNewCrv)
            
            rs.ScaleObject(strNewCrv,cMid,(rScale,rScale,rScale) )
            
            
            rSd = r.randint(1, 10)
            
            #addCurve (strNewCrv, distMin, distMax, arrVolume, newgens, maxGen)
            
            if rSd>2 :
                
                addCurve (strNewCrv, distMin, distMax, arrVolume, newgens, maxGen)
            
            
            if rSd>5:
                
                addCurve (strNewCrv, distMin, distMax, arrVolume, newgens, maxGen)
        
        
        
        
        
        
    

def main():
    
    arrObjects = rs.GetObjects("select start curves",4)
    
    if arrObjects is None: #Error cheking
        print "SELECT CURVES"
        return 
    
    arrVolumeIn = rs.GetObject("select Volume",16)
    
    if arrVolumeIn is None: #Error cheking
        print "SELECT Volume"
        return 

    gensMax = rs.GetInteger("input number of generations?",20)
    
    if gensMax is None: #Error cheking
        print "input #"
        return 
    
    searchMin = rs.GetReal("Input Min Dist to Search",10)
    
    if searchMin is None: #Error cheking
        print "input #"
        return 
    
    
    searchMax = rs.GetReal("input Max Dist to search",20)
    
    if searchMax is None: #Error cheking
        print "input #"
        return 


    rs.EnableRedraw(False)

    for i in range (len(arrObjects)):
        
        addCurve(arrObjects[i], searchMin, searchMax, arrVolumeIn, 0, gensMax)

    rs.EnableRedraw(True)




main()
