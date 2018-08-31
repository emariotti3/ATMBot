import numpy as np

class Point():
    def __init__(self,x,y):
        self.LAT = x
        self.LNG = y

    def latitude(self):
        return self.LAT

    def longitude(self):
        return self.LNG

    def getCoordRad(self):
        return [np.radians(self.LAT),np.radians(self.LNG)]

    def __str__(self):
        return "(LAT:"+str(self.LAT)+","+"LNG:"+str(self.LNG)+")"
