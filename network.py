from socket import *
import re,time
from SimpleXMLRPCServer import *
from threading import Thread

class Network(object):
    def __init__(self, config,log):
        self.log = log
        
        xmlport = config.getValue("xmlport")
        xmlhost = config.getValue("xmlhost")
        udpport = config.getValue("udpport")
        udphost = config.getValue("udphost")

        self.xml = SimpleXMLRPCServer((xmlhost, xmlport))
        self.udp = netServer(udphost,udpport,log)

        log.StartupMessage("* Attempting to start XML-RPC Server")
        self.udp.serve_forever()
        self.xmlThread = Thread( target = self.startXMLRPCServer )
        self.xmlThread.setDaemon( True )
        self.xmlThread.start()
        log.StartupMessage( "    XML-RPC Server is up at port %d" % xmlport)
        
    def register_function(self,func,funcname):
        self.xml.register_function(func,funcname)
        self.udp.register_function(func,funcname)
        self.log.Notice("Registered funtion %s for network access" % funcname)

    def stopServices(self):
        self.udp.stopServer()
        self.udp.join()
        
        self.log.StartupMessage("* Attempting to stop XML-RPC Server")
        self.xml.server_close()
        #self.xmlThread.join()

    def startXMLRPCServer(self):
        self.xml.serve_forever()


class netServer(Thread):
    def __init__(self,host,port,log):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.FUNCTIONS = {}
        self.runServer = True
        self.log = log
    
    def register_function(self,func,funcname):
        self.FUNCTIONS[funcname] = func
    
    def run(self):
        while self.runServer:
            try:
                time.sleep(0.02)
                message,addr = self.sock.recvfrom(4096)
                if type(message) is str and message != "":
                    p = re.compile("([\w]*)\(([\w,. ]*)\)")
                    ls = p.findall(message)
                    if len(ls) == 0:
                        self.log.Notice("Recieved incorrect UDP-RPC request")
                        continue
                        
                    funcname, funcargs = ls[0]
                    funcargs = funcargs.split(",")

                    if self.FUNCTIONS.has_key(funcname):
                        self.log.Notice("Recieved UDP-RPC request for function: %s" % funcname);
                        retval = self.FUNCTIONS[funcname](*funcargs)
                        self.sendData(retval, addr)
                    else:
                        self.log.Warning("Recieved UDP-RPC request for non exsistent function!")

            except Exception, e:
                try:
                    (errno,errstr) = e
                except:
                    errno = -1
                    errstr = e
                    
                if errno != 11:
                    self.log.Warning("Error recieving udp package:\n'%s'" % errstr)
                
            
    def stopServer(self):
        self.log.StartupMessage("* Attempting to stop UDP server...")
        self.runServer = False

    def sendData(self,data,addr):
        numSent = self.sock.sendto(str(data),addr)
        #if numSent != len(data):
         #   self.sendData(data,addr)
            
    def serve_forever(self):
        self.log.StartupMessage("* Attempting to start UDP server...")
        try:
            self.sock = socket(AF_INET, SOCK_DGRAM)
            self.sock.bind((self.host, self.port))
            self.sock.setblocking(False)
            self.log.StartupMessage("   UDP server is up at port %d" % self.port)
            self.start()
        except:
            self.log.StartupMessage("   Error openening UDP port %d" % self.port)
 
