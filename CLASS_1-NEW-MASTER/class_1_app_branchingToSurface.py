import rhinoscriptsyntax as rs
import math
import random



def main():
    
    attractorSurface = rs.GetObject("select Surface Please",8)
    if attractorSurface is None:return 
    
    rs.EnableRedraw(False)
    
    
    SurfaceTensor(attractorSurface,.5,.5)
    
    ptStart = rs.AddPoint(0,0,0)
    vecDir = [0,0,1]
    
    minTwigCount = 5
    maxTwigCount = 6
    maxGen = 60
    maxTwigLength = 100
    lengthMutation = .5
    maxTwigAngle = 180
    angleMutation = .5
    
    
    props = minTwigCount, maxTwigCount, maxGen, maxTwigLength, lengthMutation,maxTwigAngle, angleMutation
    
    RecursiveGrowth(ptStart, vecDir, props, 0,attractorSurface)
    
    rs.EnableRedraw(True)

def getClosestPointOnMesh(point, mesh):
    data = rs.MeshClosestPoint(mesh,point)
    return data[0]

def getClosestPointOnSurface(point, surface):
    data = rs.BrepClosestPoint(surface,point)
    return data[0]
    
def getParameterOfClosestPt(point,surface):
    data = rs.SurfaceClosestPoint(surface,point)
    return data
    
def AddArcDir(ptStart, ptEnd, vecDir):
    vecBase = rs.PointSubtract(ptEnd, ptStart)
    if rs.VectorLength(vecBase)==0.0: return
    if rs.IsVectorParallelTo(vecBase, vecDir): return
    vecBase = rs.VectorUnitize(vecBase)
    vecDir = rs.VectorUnitize(vecDir)
    vecBisector = rs.VectorAdd(vecDir, vecBase)
    vecBisector = rs.VectorUnitize(vecBisector)
    dotProd = rs.VectorDotProduct(vecBisector, vecDir)
    midLength = (0.5*rs.Distance(ptStart, ptEnd))/dotProd
    vecBisector = rs.VectorScale(vecBisector, midLength)
    #return rs.AddArc3Pt(ptStart, rs.PointAdd(ptStart, vecBisector), ptEnd)
    return rs.AddLine(ptStart,ptEnd)



def RandomPointInCone(origin, direction, minDistance, maxDistance, maxAngle):
    vecTwig = rs.VectorUnitize(direction)
    vecTwig = rs.VectorScale(vecTwig, minDistance + random.random()*(maxDistance-minDistance))
    MutationPlane = rs.PlaneFromNormal((0,0,0), vecTwig)
    vecTwig = rs.VectorRotate(vecTwig, random.random()*maxAngle, MutationPlane[1])
    vecTwig = rs.VectorRotate(vecTwig, random.random()*360, direction)
    return rs.PointAdd(origin, vecTwig)



def RecursiveGrowth(ptStart, vecDir, props, gen, srf):
    minTwigCount, maxTwigCount, maxGen, maxTwigLength, lengthMutation,maxTwigAngle, angleMutation = props
    
    if gen > maxGen : return
    
    newProps = props
    
    maxTwigLength *= lengthMutation
    maxTwigAngle *= angleMutation
    
    if maxTwigAngle>90:maxTwigAngle=90
    
    newProps = minTwigCount, maxTwigCount, maxGen, maxTwigLength, lengthMutation,maxTwigAngle, angleMutation
    
    maxN=int(minTwigCount+random.random()* (maxTwigCount-minTwigCount) )
    
    for n in range(0,maxN):
        surfaceParamter = getParameterOfClosestPt(ptStart, srf)
        srfVec = SurfaceTensor(srf, surfaceParamter[0],surfaceParamter[1])
        srfPoint = rs.EvaluateSurface(srf,surfaceParamter[0],surfaceParamter[1])
        
        vecGrowth = rs.VectorCreate(srfPoint,ptStart)
        
        if vecGrowth.Length > 5 :
            vecDir=vecGrowth
        else:
            vecDir = srfVec
        
        newPoint = RandomPointInCone(ptStart, vecDir, .25*maxTwigLength, maxTwigLength, maxTwigAngle)
        newTwig = AddArcDir(ptStart, newPoint, vecDir)
        if newTwig:
            vecGrow = rs.CurveTangent(newTwig, rs.CurveDomain(newTwig)[1])
            RecursiveGrowth(newPoint, vecGrow, newProps, gen+1,srf)
            
            
            

def SurfaceTensor(idSrf,U, V):
    localCurvature = rs.SurfaceCurvature(idSrf,(U,V))
    vecDir = localCurvature[3]
    return vecDir
    
    


if __name__ == "__main__":
    main()




