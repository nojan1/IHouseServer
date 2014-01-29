from modulewrapper import ModuleBase

class module(ModuleBase):
    def __init__(self, obj):
        ModuleBase.__init__(self)
        self.active = False
        self.obj = obj

        obj.Network.register_function(self.getAlarmActiveStatus, "getAlarmActiveStatus")
        obj.Network.register_function(self.setAlarmStatus, "setAlarmStatus")
        obj.Network.register_function(self.checkAlarmPasscode, "checkAlarmPasscode")

    def run(self, obj):
        if self.active:
            pass

    def getAlarmActiveStatus(self):
        return self.active

    def setAlarmStatus(self, newstatus, passcode):
        if self.checkAlarmPasscode(passcode):
            self.active = newstatus
            if newstatus:
                self.obj["motion"].startAll()
            else:
                self.obj["motion"].stopAll()
        else:
            self.obj.log.Warning("Incorrect password send to change alarm status")
            
    def checkAlarmPasscode(self, passcode):
        return True
        #return (self.obj.config.get("alarmpasscode") == passcode):
        
