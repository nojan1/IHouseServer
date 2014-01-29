from modulewrapper import ModuleBase
import time

class module(ModuleBase):
    def __init__(self, mao):
        ModuleBase.__init__(self)

        self.starttime = time.time()
        mao.Network.register_function(self.gettime,"uptime")

    def gettime(self):
        timedelta = self.starttime - time.time()
        
        return timedelta
