from modulewrapper import ModuleBase
import time

class module(ModuleBase):
    def __init__(self, obj):
        ModuleBase.__init__(self)
        self.setTemp = 20
        self.lastRunTime = 0

    def run(self,obj):
        SECS = time.time()
        if SECS - self.lastRunTime > 60:
            self.lastRunTime = SECS
            curHeatSetting = obj.HAL.get("ElementSetting")
            dt = self.setTemp - obj.HAL.get("InsideTemp")
            if dt > 2:
                curHeatSetting += 10
            elif dt < 2:
                curHeatSetting -= 10

            obj.HAL.set("ElementSetting",curHeatSetting)        
