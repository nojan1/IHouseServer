import os,os.path,sys

class HAL(object):
    def __init__(self,config,log):
        self.config = config
        self.log = log
        self.eventhandlers = {}
        self.loadInterfaces(config)
        self.initInterfaces()

        sys.path.append(os.path.join(os.getcwd(), "interfaces/"))

    def initInterfaces(self):
        for i in self.interfaces:
            if self.interfaces[i].init() != True:
                self.log.Error("ERROR: Interface wrapper ",self.interfaces[i].__name__,"failed to start!")

    def closeInterfaces(self):
        for i in self.interfaces:
            try:
                self.interfaces[i].close()
            except:
                self.log.Error("Error while closing interface" +self.interfaces[i].__name__ + "\n   -" + str(sys.exc_info()[1]) + "\n")

    def loadInterfaces(self,config):
        self.interfaces = {}
        for i in config.getInterfaces():
            try:
                ainterface = __import__(str(i[1]).strip())
                if i[2] == "None":
                    tmp = ainterface.Interface()
                else:
                    tmp = ainterface.Interface(*i[2].split(","))                    
                self.interfaces[i[0]] = tmp
            except:
                self.log.Error("Error in interface " + str(i[1]) + "\n" + str(sys.exc_info()[1]))
        
    def checkChanged(self):
        changed = []
        for i in self.interfaces:
            for e in self.interfaces[i].get_changed():
                if self.eventhandlers.has_key(e):
                    self.eventhandlers[e][0](*self.eventhandles[e][1])

    def register_event(self, addr, func, args = []):
        self.eventhandlers[addr] = (func, args)
        self.log.Notice("Registered event on %s to function: %s" % (addr, func.__name__))

    def get(self, *args):
        interface,addr = self.config.getInfoFromAddress(args[0])
        if len(args) == 1:
            return self.interfaces[interface].get(addr)
        else:
            return self.interfaces[interface].get(addr,*args[1:])

    def set(self, *args):
        interface,addr = self.config.getInfoFromAddress(args[0])
        if len(args) == 2 :
            return self.interfaces[interface].set(addr,args[1])
        else:
            return self.interfaces[interface].set(addr,args[1],*args[2:])

class InterfaceBase(object):
    def __init__(self):
        self.__name__ = ""

    def init(self):
        return True

    def get(self, a1):
        return None

    def set(self ,a1,a2):
        return False

    def update(self):
        pass

    def get_changed(self):
        return []

    def close(self):
        return True
