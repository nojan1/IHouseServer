from modulewrapper import ModuleBase
from subprocess import Popen

SPEACHCOMMAND = "espeak -v en+f4 %s"

class module(ModuleBase):
    def __init__(self, mao):
        ModuleBase.__init__(self)

        self.speachproc = None
        self.speachbuffer = []

        mao.Network.register_function(self.say, "speach")

    def say(self, text):
        self.speachbuffer.append(text)
        return True
    
    def run(self, mao):
        if len(self.speachbuffer) > 0:
            if self.speachproc == None or self.speachproc.poll() != None:
                command = SPEACHCOMMAND.replace("%s", self.speachbuffer.pop(0)).split(" ")
                self.speachproc = Popen(command)
