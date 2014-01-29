from modulewrapper import ModuleBase
from subprocess import *
import urllib

class module(ModuleBase):
    def __init__(self, mao):
        ModuleBase.__init__(self)
        self.mao = mao
        return

        mao.Network.register_function(self.startAll, "startMotion")
        mao.Network.register_function(self.stopAll, "stopMotion")

        self.proc = self.startProcess()
        self.stopAll()

    def startProcess(self):
        self.mao.Log.Notice("Attempting to start motion subprocess")
        return Popen(["motion"], stdout=PIPE, stderr=PIPE)

    def startAll(self):
        self.detectionCommand("start")

    def stopAll(self):
        self.detectionCommand("pause")

    def detectionCommand(self,type):
        for i in range(4):
          ret = self.sendCommand("%d/detection/%s" % (i,type))
          if "Done" not in ret:
              self.mao.Log.Warning("Failed to %s motion thread %d" % (type,i))

    def sendCommand(self, command):
        port = self.mao.Config.getValue("motionport")
        try:
            f = urllib.urlopen("http://localhost:%d/%s" % (port, command))
            return f.read()
        except Exception,e:
            self.mao.Log.Warning("Error processing command (%s):\n%s" % (command,e))
            return ""

    def run(self, mao):
        return
        self.proc.poll()
        if self.proc.returncode != None:
            self.mao.Log.Warning("Motion subprocss seems to have died, restarting")
            self.proc = self.startProcess()
        

    def close(self):
        self.proc.terminate()
