import rhinoscriptsyntax as rs
import Rhino


class Particle:
    
    def __init__(self, size, location, vel, acc):
        self._size = size
        self._loc = location
        self._vel = vel
        self._acc = acc
        self._bBox = None
        self._alive = True
    
    def setBoundingBox(self,boundingBox):
        self._bBox = boundingBox
        
    def update(self):
        self._vel = rs.VectorAdd(self._vel,self._acc)
        self._loc = rs.VectorAdd(self._loc, self._vel)
        if(self._bBox and not self._bBox.Contains(Rhino.Geometry.Point3d(self._loc))):
            self._alive = False
    
    def draw(self):
        if(self._alive):
            return rs.AddPoint(self._loc)
        else:
            return False
