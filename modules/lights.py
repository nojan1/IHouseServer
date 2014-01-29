from modulewrapper import ModuleBase

class module(ModuleBase):
     def __init__(self, obj):
          ModuleBase.__init__(self)
     
     def run(self,obj):
          obj.HAL.set("StairLight", obj.HAL.get("StairLightSwitch"))
