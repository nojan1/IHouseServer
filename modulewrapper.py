import os,sys,time

class MAO(object):
    def __init__(self):
        self.HAL = None
        self.Network = None
        self.Log = None
        self.Config = None
        self.modules = None

    def __getitem__(self, key):
        key = "modules/%s" % key
        if self.modules.has_key(key):
            return self.modules[key]
        else:
            raise TypeError("%s not found" % key)

class Modulewrapper(object):
    def __init__(self):
        sys.path.append("modules/");
        self.modules = {}

    def loadModule(self,argmodule,obj):
        path = os.path.join("modules/",argmodule)
        if os.path.exists(path) or os.path.exists(path+".py"):
            if path[-2:] == "py":
                try:
                    m = __import__(argmodule)
                    self.modules[argmodule] = m.module(obj)
                    obj.Log.Notice("Module %s loaded successfully" % argmodule)
                except Exception,e:
                    obj.Log.Error("Error in %s\n%s" % (argmodule,str(e)))
        else:
            obj.Log.Error("Module %s not found" % argmodule)

    def loadModules(self,obj):
        self.modules = {}
        files = os.listdir("modules/")
        for f in files:
            if f[-2:] == "py":
                try:
                    f=f[:-3]
                    amodule = __import__(f)
                    self.modules[f] = amodule.module(obj)
                except Exception,e:
                    obj.Log.Error("Error in %s\n%s" % (f,e))

    def runModules(self,obj):
        for m in self.modules:
            try:
                if self.modules[m].errorflag == None or (time.time() - self.modules[m].errorflag) > 60:
                    self.modules[m].run(obj)
            except Exception,e :
                obj.Log.Error("Error running module %s, suspended for 1 minute\n   - %s\n" % (m, e))
                self.modules[m].errorflag = time.time()

    def stopModules(self,obj):
        for m in self.modules:
            try:
                self.modules[m].close()
            except Exception,e:
                obj.Log.Error("Error closing module %s:\n%s" % (m,e))


class ModuleBase(object):
    def __init__(self):
        self.errorflag = None

    def run(self, mao):
        pass

    def close(self):
        pass
