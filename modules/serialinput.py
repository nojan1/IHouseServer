from modulewrapper import ModuleBase
import serial,re

class module(ModuleBase):
    def __init__(self, mao):
        ModuleBase.__init__(self)
        self.buffer = ""
        self.regexp = re.compile('([\w\d]+)\(([\w\d,"]*)\)')

        try:
            portname = mao.Config.getValue("serialcontrolport")
            self.port = serial.Serial(portname, 9600, EIGHTBITS, PARITY_NONE, STOPBITS_ONE, 0)
        except:
            mao.Log.Warning("Failed to open serial port for serial control")
            self.port = None

    def run(self, mao):
        if self.port != None:
            self.buffer += self.port.read()
            res = self.regexp.findall(self.buffer)
            if len(res) > 0:
                funcname = res[0]
                funcargs = res[1].split(",")
                if mao.Network.udp.FUNCTIONS.has_key(funcname):
                    retval = mao.Network.udp.FUNCTIONS[funcname](*funcargs)
                    self.port.write(retval)
                length = len(funcname) + len(res[1]) + 2
                self.buffer = self.buffer[length:]
            else:
                mao.log.Notice("Recieved serial request for non existent function: %s" & funcname)
