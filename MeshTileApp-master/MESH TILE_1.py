import rhinoscriptsyntax as Rhino
import math as m
import random as r


def Main():

    heightScale = Rhino.GetReal("input height scale", .05)


    
    strObject = Rhino.GetObject("Select mesh", 32)
    
    arrFaces = Rhino.MeshFaces(strObject, False)
    arrMeshFaceVertices = Rhino.MeshFaceVertices(strObject)
    
    arrMeshVerticesIn = Rhino.MeshVertices(strObject)
    arrMeshVertexNrmls = Rhino.MeshVertexNormals(strObject)
    
    
    meshFaceCount = Rhino.MeshFaceCount(strObject)
    arrAllMeshNormals = Rhino.MeshFaceNormals(strObject)
    
    
    #Rhino.EnableRedraw False
    Rhino.AddLayer ("sCrvs")

    if IsArray(arrFaces):
        
        Rhino.EnableRedraw (False)


        for i in range(0, meshFaceCount ):

            Rhino.Prompt (str(i) + "_" + str(meshFaceCount))
            
            arrMeshVertexIndices = [arrMeshFaceVertices[i][0],arrMeshFaceVertices[i][1],arrMeshFaceVertices[i][2]]
            arrFace=[]
            
            #arrMeshVertexIndices[0] = arrMeshFaceVertices[i][0]
            #arrMeshVertexIndices[1] = arrMeshFaceVertices[i][1]
            #arrMeshVertexIndices[2] = arrMeshFaceVertices[i][2]
            
            arrFace.append( arrMeshVerticesIn[arrMeshVertexIndices[0]])
            arrFace.append(arrMeshVerticesIn[arrMeshVertexIndices[1]])
            arrFace.append(arrMeshVerticesIn[arrMeshVertexIndices[2]])
            arrFace.append(arrMeshVerticesIn[arrMeshVertexIndices[0]])
            
            strLineT = Rhino.AddPolyline(arrFace)
            
            nrml1 = arrMeshVertexNrmls[arrMeshVertexIndices[0]]
            nrml2 = arrMeshVertexNrmls[arrMeshVertexIndices[1]]
            nrml3 = arrMeshVertexNrmls[arrMeshVertexIndices[2]]
            
            #Rhino.AddPoint (Rhino.VectorAdd(arrFaces[i], nrml1))
            #Rhino.AddPoint (Rhino.VectorAdd(arrFaces[i + 1], nrml2))
            #Rhino.AddPoint (Rhino.VectorAdd(arrFaces[i + 2], nrml3))
            
            if	Rhino.IsCurveClosed(strLineT):
                crvLength = Rhino.CurveLength(strLineT)
                srf = Rhino.AddPlanarSrf(strLineT)
                if IsArray(srf) :
                    areaData = Rhino.SurfaceAreaCentroid(srf[0])
                    if IsArray(areaData):
                        srfClosestPt = Rhino.SurfaceClosestPoint(srf[0], areaData[0])
                        nrml = arrAllMeshNormals[i]
                        Rhino.DeleteObject( srf[0])
                        arrSrfPoints = arrFace
                        
                        crv1 = Rhino.AddLine(arrSrfPoints[0], arrSrfPoints[1])
                        crv2 = Rhino.AddLine(arrSrfPoints[1], arrSrfPoints[2])
                        crv3 = Rhino.AddLine(arrSrfPoints[2], arrSrfPoints[0])
                        
                        arrSharedFaces1 = Rhino.MeshVertexFaces(strObject, arrMeshVertexIndices[0])
                        arrSharedFaces2 = Rhino.MeshVertexFaces(strObject, arrMeshVertexIndices[1])
                        arrSharedFaces3 = Rhino.MeshVertexFaces(strObject, arrMeshVertexIndices[2])
                        neighborNrml1 = arrAllMeshNormals[getNeighborMeshFaceNormal(arrSharedFaces1, arrSharedFaces2, i)]
                        neighborNrml2 = arrAllMeshNormals[getNeighborMeshFaceNormal(arrSharedFaces2, arrSharedFaces3, i)]
                        neighborNrml3 = arrAllMeshNormals[getNeighborMeshFaceNormal(arrSharedFaces3, arrSharedFaces1, i)]
                        
                        lCrv1 = Rhino.AddLine(Rhino.CurveEndPoint(crv1), areaData[0])
                        lCrv2 = Rhino.AddLine(Rhino.CurveEndPoint(crv2), areaData[0])
                        lCrv3 = Rhino.AddLine(Rhino.CurveEndPoint(crv3), areaData[0])
                        
                        
                        c1D = Rhino.CurveDomain(crv1)
                        c2D = Rhino.CurveDomain(crv2)
                        c3D = Rhino.CurveDomain(crv3)
                        
                        
                        d1 = c1D[0] + ((c1D[1] - c1D[0] ) / 2)
                        d2 = c2D[0] + ((c2D[1] - c2D[0] ) / 2)
                        d3 = c3D[0] + ((c3D[1] - c3D[0] ) / 2)
                        
                        mPt1 = Rhino.EvaluateCurve(crv1, d1)
                        mPt2 = Rhino.EvaluateCurve(crv2, d2)
                        mPt3 = Rhino.EvaluateCurve(crv3, d3)
                        
                        C1a1Pt = evalCrv(crv1, .5 +(.5 / 8.5))
                        C1a2Pt = evalCrv(crv1, .5 -( .5 / 8.5))
                        C1b1Pt = evalCrv(crv1, .5 +(.5 / 2))
                        C1b2Pt = evalCrv(crv1, .5 -( .5 / 2))
                        
                        C2a1Pt = evalCrv(crv2, .5 +(.5 / 8.5))
                        C2a2Pt = evalCrv(crv2, .5 -( .5 / 8.5))
                        C2b1Pt = evalCrv(crv2, .5 +(.5 / 2))
                        C2b2Pt = evalCrv(crv2, .5 -( .5 / 2))
                        
                        C3a1Pt = evalCrv(crv3, .5 +(.5 / 8.5))
                        C3a2Pt = evalCrv(crv3, .5 -( .5 / 8.5))
                        C3b1Pt = evalCrv(crv3, .5 +(.5 / 2))
                        C3b2Pt = evalCrv(crv3, .5 -( .5 / 2))
                        
                        
                        nrmlC1 = Rhino.VectorScale(Rhino.VectorAdd(nrml, neighborNrml1), Rhino.CurveLength(crv1) * heightScale)
                        
                        c1CL = Rhino.AddLine(mPt1, areaData[0])
                        C1LC1 = Rhino.CopyObject(c1CL, Rhino.VectorCreate(mPt1, C1a1Pt))
                        C1LC1 = Rhino.MoveObject(C1LC1, Rhino.VectorCreate(C1a1Pt, Rhino.VectorAdd(C1a1Pt, nrmlC1)))
                        
                        C1LC2 = Rhino.CopyObject(c1CL, Rhino.VectorCreate(mPt1, C1a2Pt))
                        C1LC2 = Rhino.MoveObject(C1LC2, Rhino.VectorCreate(C1a2Pt, Rhino.VectorAdd(C1a2Pt, nrmlC1)))
                        
                        C1LC3 = Rhino.CopyObject(c1CL, Rhino.VectorCreate(mPt1, C1b1Pt))
                        
                        C1LC4 = Rhino.CopyObject(c1CL, Rhino.VectorCreate(mPt1, C1b2Pt))
                        
                        nrmlC2 = Rhino.VectorScale(Rhino.VectorAdd(nrml, neighborNrml2), Rhino.CurveLength(crv2) * heightScale)
                        c2CL = Rhino.AddLine(mPt2, areaData[0])
                        
                        C2LC1 = Rhino.CopyObject(c2CL, Rhino.VectorCreate(mPt2, C2a1Pt))
                        
                        C2LC1 = Rhino.MoveObject(C2LC1, Rhino.VectorCreate(C2a1Pt, Rhino.VectorAdd(C2a1Pt, nrmlC2)))
                        
                        C2LC2 = Rhino.CopyObject(c2CL, Rhino.VectorCreate( mPt2, C2a2Pt))
                        C2LC2 = Rhino.MoveObject(C2LC2, Rhino.VectorCreate(C2a2Pt, Rhino.VectorAdd(C2a2Pt, nrmlC2)))
                        
                        C2LC3 = Rhino.CopyObject(c2CL, Rhino.VectorCreate(mPt2, C2b1Pt))
                        
                        C2LC4 = Rhino.CopyObject(c2CL, Rhino.VectorCreate(mPt2, C2b2Pt))
                        
                        nrmlC3 = Rhino.VectorScale(Rhino.VectorAdd(nrml, neighborNrml3), Rhino.CurveLength(crv3) * heightScale)
                        c3CL = Rhino.AddLine(mPt3, areaData[0])
                        
                        C3LC1 = Rhino.CopyObject(c3CL, Rhino.VectorCreate(mPt3, C3a1Pt))
                        C3LC1 = Rhino.MoveObject(C3LC1, Rhino.VectorCreate(C3a1Pt, Rhino.VectorAdd(C3a1Pt, nrmlC3)))
                        
                        C3LC2 = Rhino.CopyObject(c3CL, Rhino.VectorCreate(mPt3, C3a2Pt))
                        C3LC2 = Rhino.MoveObject(C3LC2, Rhino.VectorCreate(C3a2Pt, Rhino.VectorAdd(C3a2Pt, nrmlC3)))
                        
                        C3LC3 = Rhino.CopyObject(c3CL, Rhino.VectorCreate(mPt3, C3b1Pt))
                        
                        C3LC4 = Rhino.CopyObject(c3CL,Rhino.VectorCreate( mPt3, C3b2Pt))
                        
                        
                        #'''''FINAL POINTS ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                        #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                        
                        cc1a=[0,0,0,0,0]
                        cc1b=[0,0,0,0,0]
                        cc2a=[0,0,0,0,0]
                        cc2b=[0,0,0,0,0]
                        cc3a=[0,0,0,0,0]
                        cc3b=[0,0,0,0,0]
                        
                        
                        cc1a [0] = evalCrv(C1LC2, 0)
                        cc1a[1] = evalCrv(C1LC2, .5)
                        
                        cc1a[2] = evalCrv(lCrv1, .55)
                        
                        cc1a[3] = evalCrv(C2LC4, .5)
                        cc1a[4] = evalCrv(C2LC4, 0)
                        
                        
                        cc1b[0] = evalCrv(C1LC1, 0)
                        
                        test= evalCrv(C1LC1, .5)
                        cc1b[1] = Rhino.VectorSubtract(test, nrmlC1)
                        
                        test = evalCrv(lCrv3, .5)
                        cc1b[2] = Rhino.VectorSubtract(test, nrmlC1)
                        
                        cc1b[3] = evalCrv(C3LC3, .125)
                        cc1b[4] = evalCrv(C3LC3, 0)
                        
                        
                        cc2a[0] = evalCrv(C2LC2, 0)
                        cc2a[1] = evalCrv(C2LC2, .5)
                        
                        cc2a[2] = evalCrv(lCrv2, .55)
                        
                        cc2a[3] = evalCrv(C3LC4, .5)
                        cc2a[4] = evalCrv(C3LC4, 0)
                        
                        cc2b[0] = evalCrv(C2LC1, 0)
                        
                        test = evalCrv(C2LC1, .5)
                        cc2b[1] = Rhino.VectorSubtract(test, nrmlC2)
                        
                        test = evalCrv(lCrv1, .5)
                        cc2b[2] = Rhino.VectorSubtract(test, nrmlC2)
                        
                        cc2b[3] = evalCrv(C1LC3, .125)
                        cc2b[4] = evalCrv(C1LC3, 0)
                        
                        
                        cc3a[0] = evalCrv(C3LC2, 0)
                        cc3a[1] = evalCrv(C3LC2, .5)
                        
                        cc3a[2] = evalCrv(lCrv3, .55)
                        
                        cc3a[3] = evalCrv(C1LC4, .5)
                        cc3a[4] = evalCrv(C1LC4, 0)
                        
                        
                        cc3b[0] = evalCrv(C3LC1, 0)
                        
                        test = evalCrv(C3LC1, .5)
                        cc3b[1] = Rhino.VectorSubtract(test, nrmlC3)
                        
                        test = evalCrv(lCrv2, .5)
                        cc3b[2] = Rhino.VectorSubtract(test, nrmlC3)
                        
                        cc3b[3] = evalCrv(C2LC3, .125)
                        cc3b[4] = evalCrv(C2LC3, 0)
                        
                        curve1 = Rhino.AddCurve(cc1a)
                        
                        #curve2 = Rhino.AddCurve(cc1b)
                        
                        #curve3 = Rhino.AddCurve(cc2a)
                        
                        #curve4 = Rhino.AddCurve(cc2b)
                        
                        #curve5 = Rhino.AddCurve(cc3a)
                        
                        #curve6 = Rhino.AddCurve(cc3b)
                        
                        Rhino.ObjectLayer (curve1, "sCrvs")
                        #Rhino.ObjectLayer (curve2, "sCrvs")
                        #Rhino.ObjectLayer (curve3, "sCrvs")
                        #Rhino.ObjectLayer (curve4, "sCrvs")
                        #Rhino.ObjectLayer (curve5, "sCrvs")
                        #Rhino.ObjectLayer (curve6, "sCrvs")
                        
                        
                        Rhino.DeleteObjects([C1LC1, C2LC1, C3LC1, C1LC2, C2LC2, C3LC2, C1LC3, C2LC3, C3LC3, C1LC4, C2LC4, C3LC4])
                        Rhino.DeleteObjects([lCrv1, lCrv2, lCrv3,crv1,crv2,crv3])
                        Rhino.DeleteObjects([c1CL, c2CL, c3CL])
                    else:
                        Rhino.DeleteObject (srf[0])
                    
                
            
        
    Rhino.EnableRedraw (True)
    
    
    #RHINO.SelectObject (crv1)



def getNeighborMeshFaceNormal(arrShared1, arrShared2, testFace):
    neighborFace = arrShared1[0]
    blnShared = False
    for i in range(0,len(arrShared1)):
        if not blnShared:
            if not arrShared1[i] == testFace:
                for j in range(0,len(arrShared2)):
                    if not blnShared:
                        if not arrShared2[j] == testFace:
                            if arrShared1[i] == arrShared2[j]:
                                blnShared = True
                                neighborFace = arrShared1[i]
                                
    return neighborFace



def getMeshNormalFromCurve(strCrv, StrMesh, arrCntr):

    meshFaceVertices = Rhino.MeshFaceVertices(StrMesh)
    meshClosestPt = Rhino.MeshClosestPoint(StrMesh, arrCntr)
    verticesOfTestFace = meshFaceVertices(meshClosestPt(1))





def evalCrv(strCrv, Parameter):
    domain = Rhino.CurveDomain(strCrv)
    newP = domain[0] + ((domain[1] - domain[0]) * Parameter)
    return Rhino.EvaluateCurve(strCrv, newP)
	





def IsArray(var):
    return isinstance(var, (list, tuple))
    
    
    
Main()