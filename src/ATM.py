class ATM():
    def __init__(self,id,point,network,bank,address):
        self.id=id
        self.loc=point
        self.network=network
        self.bank=bank
        self.address=address

    def getLoc(self):
        return self.loc

    def getBank(self):
        return self.bank

    def getNetwork(self):
        return self.network

    def getAddress(self):
        return self.address

    def __str__(self):
        return "{ id:"+str(self.id)+",loc:"+str(self.loc)+",network:"+str(self.network)+",bank:"+(str(self.bank))+"}"
