from curses import *
import curses.textpad
from modulewrapper import *
from config import *
import sys,time

class OutputClass(object):
    def __init__(self,scrn):
        self.scrn = scrn
        self.win = newwin(0,0)

    def refresh(self):
        self.win.redrawwin()
        self.win.refresh()
        
    def printer(self, msg):
        pos = getsyx()
        self.win.addstr(msg)
        setsyx(pos[0]+1, pos[1])
        self.refresh()
        print msg

class DummyHAL(object):
    def __init__(self,log):
        self.log = log
        self.dummies = {}

    def set(self, *args):
        self.dummies[args[0]] = args[1]
        return True

    def get(self, *args):
        if self.dummies.has_key(args[0]):
            return self.dummies[args[0]]
        else:
            return 0

    def register_event(self,addr,func,args=[]):
        self.log.Notice("Tried to regist event, not yet possible in simmulation")

class DummyLog(object):
    def __init__(self, neat):
        self.output = neat

    def Error(self, msg):
        self.output.printer("Error: "+msg)
        
    def Notice(self, msg):
        self.output.printer("Notice: "+msg)

    def Warning(self, msg):
        self.output.printer("Warning: "+msg)

class DummyNetwork(object):
    def register_function(self, func, bla):
        pass

class MainApp(object):
    def __init__(self):
        pass

    def run(self,scrn):
        self.output = OutputClass(scrn)
        
        config = Config()
        log  = DummyLog(self.output)
        hal = DummyHAL(log)
        net = DummyNetwork()

        self.mao = MAO()
        self.mao.HAL = hal
        self.mao.Network = net
        self.mao.Log = log
        self.mao.Config = config

        self.modules = Modulewrapper()
        if len(sys.argv) > 1:
            for m in sys.argv[1:]:
                self.modules.loadModule(m,self.mao)
        else:
            sys.exit(0)

        run = True
        paused = False
        clock = 0.1

        scrn.nodelay(True)
        
        while run:
            time.sleep(clock)
            
            i = scrn.getch()
            if i == ord("q"):
                run = False
            elif i == ord("i"):
                text = curses.textpad.Textbox(self.output.win)
                command = text.edit()
                first = command.split(" ").toupper()
                if first == "GET":
                    flash()
                elif first == "SET":
                    pass
                
            elif i == ord("p"):
                paused = not paused

            if not paused:
                self.modules.runModules(self.mao)

        self.modules.stopModules(self.mao)

if __name__ == "__main__":
    app = MainApp()
    wrapper(app.run)
