from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import urlparse,cgi,re

validpages = ["adminindex","admininterfaces","adminconfigvalues","adminiobindings","adminutilities"]

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        dicti = {}
        parsed_path = urlparse.urlparse(self.path)
        for v in parsed_path.query.split("&"):
            if v != "":
                key,val = v.split("=")
                dicti[key] = val
        self.doHandle(dicti)

    def doHandle(self,dict):
        try:
            if self.path == "/":
                self.path = "adminindex"
            else:
                tmp = re.findall("/([\w\d]*)\?.*",self.path)
                if len(tmp) > 0:
                    self.path = tmp[0]
                else:
                    self.path = self.path[1:]
            
            if self.path in validpages:
                pageobject = __import__(self.path)
                output = pageobject.run(dict)
                self.send_response(200, "OK")
                self.send_header("Content-type","text/html")
                self.send_header("Content-length", len(output))
                self.end_headers()
                self.wfile.write(output)
                self.wfile.close()
            else:
                self.send_error(404)
        except Exception,e:
            self.send_error(500)
            print e

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        dicti = {}
        for key in form:
            if type(form[key]) is list:
                item = form[key][0].value
            else:
                item = form[key].value
            dicti[key] = item
        self.doHandle(dicti)
            
class WebAdministration(HTTPServer):
    def __init__(self,config,log):
        host = config.getValue("webadminhost")
        port = config.getValue("webadminport")
        
        HTTPServer.__init__(self,(host,port), RequestHandler)

        log.StartupMessage("* Attempting to start web administration")
        httpthread = Thread(target=self.serve_forever)
        httpthread.setDaemon(True)
        httpthread.start()
        log.StartupMessage("   Web administration is up at port %d" % port)

if __name__ == "__main__":
    try:
        server = HTTPServer(("",9000),RequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print "Exiting"
