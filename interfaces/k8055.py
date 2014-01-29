from HAL import InterfaceBase
import pyk8055

class Interface(InterfaceBase):
    def __init__(self,cardID):
        InterfaceBase.__init__(self)
        self.__name__ = "K8055 interface wrapper"
        
        self.cardID = cardID
        self.record = [0,0,0,0,0,0,0,0,0,0]

    def close(self):
        pyk8055.CloseDevice(self.cardID)
        print "* Closed connection to card%s" % str(self.cardID)

    def init(self,firstStart=1):
        res = pyk8055.OpenDevice(self.cardID)
        if firstStart == 1:
            print "* Initializing card" + str(self.cardID) + "..."
            if res == self.cardID:
                print "   Succesfully opened connection to card" + str(self.cardID)
                return True
            elif res == -1:
                print "   Error: card" + str(self.cardID) + " was not found!. Quiting!"
                return False
            else:
                print "   Error: failed to establish connection to card" + str(self.cardID) + "! Quiting"
                return False

    def get(self, addres):
        self.init(0)
        addres = int(addres)
        if addres < 10:
            return self.record[addres]
        elif addres < 15:
            return pyk8055.ReadDigitalChannel(addres)
        elif addres < 17:            
            return pyk8055.ReadAnalogChannel(addres)

    def set(self,addres,value):
        addres = int(addres)
        if addres < 10:
            self.init(0)
            self.record[addres] = value
            if addres < 8:
                if value == 1:
                    pyk8055.SetDigitalChannel(addres)
                else:
                    pyk8055.ClearDigitalChannel(addres)			
            else:
                pyk8055.SetAnalogChannel(self.record[8],self.record[9])
            return True
        else:
            print "Error: attempt to set unsetable address(" + str(addres) + ") at card+" + str(self.cardID) + "!"
            return False
