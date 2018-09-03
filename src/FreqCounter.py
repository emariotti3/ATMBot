import numpy as np
import datetime as dt
from math import ceil,e,log1p
from sklearn.utils import murmurhash3_32

HIPOTHESIS_P = 0.05
EPSILON = 0.01
ATM_MODEL = "countmin-atms{}.npy"
RELOAD_TIME = 8

def lastWeekday(d):
    date = d.date()
    while not date.weekday():
        date -= dt.timedelta(days=1)
    return date

class FreqCounter():

    def __init__(self):
        self.d = int(ceil(e/EPSILON))
        self.w = int(ceil(log1p(1/HIPOTHESIS_P)))
        date = lastWeekday(dt.datetime.now())
        if (not np.DataSource().exists(ATM_MODEL.format(str(date.day)))):
            if dt.datetime.now().hour >= RELOAD_TIME:
                self.fname = ATM_MODEL.format(str(date.day))
            else:
                self.fname = ATM_MODEL.format(str(lastWeekday(date - dt.timedelta(days=1))))
            np.save(self.fname,np.array([[0 for i in range(self.w)] for j in range(self.d)]))

    def calculate(self,atmId):
        """Given an id, returns the approximate historic frequency for that
        event.
        """
        freq = -1
        try:
            data = np.load(self.fname)
            for row in range(self.d):
                col = murmurhash3_32(atmId, seed=row, positive=True) % self.w
                freq = data[row][col] if (data[row][col] < freq or freq < 0) else freq
        except Exception, e:
            return 0
        return freq

    def increase(self,atmId):
        """Given an id, increases occurrence frequency of that item by one.
        """
        data = np.load(self.fname)
        for row in range(self.d):
            col = murmurhash3_32(atmId, seed=row, positive=True) % self.w
            data[row][col]+=1
        np.save(self.fname,data)
