import time

class logManager(object):
    def __init__(self, config):
        self.config = config
        self.msgrecord = {}
        
    def event(self, msg, level):
        if self.msgrecord.has_key(msg) and (time.time() - self.msgrecord[msg]) < 10:
            return

        self.msgrecord[msg] = time.time()
        
        loglevel = self.config.getValue("loglevel")
        printlevel = self.config.getValue("printlevel")
        logpath = self.config.getValue("logpath")

        if level < loglevel:
            f = open(logpath, "a")
            f.write("%s %s\n" % (time.asctime(),msg))
            f.close()

        if level < printlevel:
            print msg

    def Warning(self,msg):
        self.event(msg, 2)

    def Notice(self, msg):
        self.event(msg,3)

    def Error(self, msg):
        self.event(msg,1)

    def StartupMessage(self, msg):
        print msg
