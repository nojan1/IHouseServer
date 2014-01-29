from HAL import InterfaceBase
import os

OWFSMOUNTPOINT = "/dev/1wire"

class Interface(InterfaceBase):
    def __init__(self):
        InterfaceBase.__init__(self)

    def set(self, addr, value, what):
        try:
            f = open(os.path.join(OWFSMOUNTPOINT, addr, what),"w")
            f.write(value)
            f.close()
            return True
        except:
            print "Failed to open owfs file %s node %s for writing" % (addr,what)
            return False

    def get(self, addr, what):
        try:
            f = open(os.path.join(OWFSMOUNTPOINT, addr, what), "r")
            val = f.read()
            f.close()
            return val
        except:
            print "Failed to open owfs file %s node %s for reading" % (addr,what)
            return False

    
