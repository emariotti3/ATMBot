import math
import random
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree
from Point import Point
from ATM import ATM
from FreqCounter import FreqCounter

atmfile = "cajeros-automaticos.csv"
EARTH_RADIUS = 6371
NETWORKS = ["LINK","BANELCO"]
K_NEIGHBOURS = {0:(0,0.7), 1:(0.7,0.9),2:(0.9,1)}

class ATMFinder():
    instance = None
    geopoints=[]

    class __OnlyOne:
        def __init__(self,radius):
            self.radius = radius
            self.atmData = atmfile #process here
            self.freqCounter = FreqCounter()
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

    def __init__(self,radius):
        if not ATMFinder.instance:
            ATMFinder.instance = ATMFinder.__OnlyOne(radius)

    def knn(self,center,maxOps,network=""):
        """Receives a center point expressed in latitude and longitude ([lat,long]).
        Optionally receives an ATM network name.
        Returns k closest ATMs within specified radius. If a network is specified
        it will only return ATMs belonging to that network, otherwise returns top
        k ATMs found regardless of the network.
        """
        chanceConsult = random.random()
        rc = Point(center[0],center[1]).getCoordRad()
        idx,dst = ATMFinder.instance.atmTree.query_radius(np.asarray([rc]),ATMFinder.instance.radius,sort_results=True,return_distance=True)
        atms = []
        try:
            for i in idx[0].tolist():
                atm = ATMFinder.getATM(i)
                atmOps = self.instance.freqCounter.calculate(atm.getId())
                #check atm is from network and is still available for extraction
                if (atm.getNetwork() == network or len(network)==0) and atmOps < maxOps:
                    #print(math.asin(math.sqrt(dst[0][i]))*2*EARTH_RADIUS)
                    atms.append(atm)
                if len(atms) == len(K_NEIGHBOURS):
                    break
            for j in range(len(atms)):
                if chanceConsult>=K_NEIGHBOURS[j][0] and chanceConsult<K_NEIGHBOURS[j][1]:
                    self.instance.freqCounter.increase(atms[j].getId())
        except Exception, e:
            return []
        return atms
