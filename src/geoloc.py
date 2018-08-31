import math
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree
from Point import Point
from ATM import ATM

atmfile="cajeros-automaticos.csv"
EARTH_RADIUS=6371
NETWORKS=["LINK","BANELCO"]

class ATMFinder():
    instance = None
    geopoints=[]

    class __OnlyOne:
        def __init__(self,k,radius):
            self.k = k
            self.radius = radius
            self.atmData = atmfile #process here
            data = pd.read_csv(atmfile,delimiter=";",header=0)
            for atm in data.itertuples(index=True):
                atm = ATM(atm.ID,Point(eval(".".join(atm.LAT.split(","))), eval(".".join(atm.LNG.split(",")))),atm.RED,atm.BANCO,atm.DOM_ORIG)
                ATMFinder.geopoints.append(atm)
            self.atmTree = BallTree(np.asarray([atm.getLoc().getCoordRad() for atm in ATMFinder.geopoints]), leaf_size=2,metric="haversine")

    @classmethod
    def isNetwork(c,networkName):
        return networkName.upper() in NETWORKS

    @classmethod
    def getATM(c,index):
        return ATMFinder.geopoints[index]

    def __init__(self,k,radius):
        if not ATMFinder.instance:
            ATMFinder.instance = ATMFinder.__OnlyOne(k,radius)

    def knn(self,center,network=""):
        """Receives a center point expressed in latitude and longitude ([lat,long]).
        Optionally receives an ATM network name.
        Returns k closest ATMs within specified radius. If a network is specified
        it will only return ATMs belonging to that network, otherwise returns top
        k ATMs found regardless of the network.
        """
        rc = Point(center[0],center[1]).getCoordRad()
        idx,dst = ATMFinder.instance.atmTree.query_radius(np.asarray([rc]),ATMFinder.instance.radius,sort_results=True,return_distance=True)
        atms = []
        try:
            for i in idx[0].tolist():
                atm = ATMFinder.getATM(i)
                if atm.getNetwork() == network or len(network)==0:
                    #print(math.asin(math.sqrt(dst[0][i]))*2*EARTH_RADIUS)
                    atms.append(atm)
                if len(atms) == ATMFinder.instance.k:
                    return atms
        except ValueError:
        	#Apparently this is due to a problem with numpy arrays.
            #Exception should not be used to control non-exceptional flow.
            return []
        return atms
