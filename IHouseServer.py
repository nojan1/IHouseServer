#!/usr/bin/python

import string
import time
import signal
import sys
from HAL import *
from network import *
from config import *
from modulewrapper import *
from logmanager import *
from webadmin import *

class IHouseServer(object):
    
    def Main(self):
        signal.signal(signal.SIGHUP, self.reInitialize)
        print "Starting initializion sequence..."
        print "======================================================"

        try:
            config = Config()
        except:
            print "*   ERROR: initializing config module failed\n    Is the database running and accessable";
            sys.exit(1)
            
        log = logManager(config)
        hal = HAL(config,log)
        net = Network(config,log)
        web = WebAdministration(config,log)

        net.register_function(hal.get, "get")
        net.register_function(hal.set, "set")
        net.register_function(self.reInitialize, "reinitialize")
        
        #create Module Argument Object
        self.mao = MAO()
        self.mao.HAL = hal
        self.mao.Network = net
        self.mao.Log = log
        self.mao.Config = config

        self.modules = Modulewrapper()
        self.modules.loadModules(self.mao)
        self.mao.modules = self.modules.modules
        
        print "\nInitializion sequence completed, entering working mode"
        print "======================================================"
        while 1:
            try:
                self.modules.runModules(self.mao)
                hal.checkChanged()
                    
                time.sleep(0.02)
            except KeyboardInterrupt:
                break

        print "======================================================"   
        print "Program exiting...\n"
        self.modules.stopModules(self.mao)
        hal.closeInterfaces()
        net.stopServices()
        print "\nAll stopped!.. God Bye :)"

    def reInitialize(self,signum=None, frame=None):
        self.mao.Log.Notice("Recieved reinitialization request... executing")
        self.mao.HAL.closeInterfaces()
        self.mao.HAL.initInterfaces()
        self.modules.loadModules(self.mao)
    
if __name__ == "__main__":
    IHouse = IHouseServer()
    IHouse.Main()
