
DBEngine="mysql"

if DBEngine == "mysql":
    import MySQLdb as db
    from mysqlcredentials import *
else:
    import sqlite3 as db


class Config(object):
    def __init__(self):
        if DBEngine == "mysql":
            self.conn = db.connect(host,username,password,database);
        else:
            self.conn = db.connect("database")

    def getValue(self,name):
        conv={"str":str, "int":int, "float":float}
        c = self.conn.cursor()
        c.execute('select value,type from configvalues where name="%s"' % name)
        ret = c.fetchone()
        if ret == None or len(ret) == 0:
            raise Exception("Specified value (%s) does not exist" % name);
        else:
            return conv[ret[1]](ret[0])

    def setValue(self,name,value):
        c = self.conn.cursor()
        sql = 'insert into configvalues (name,value,type) values("%s","%s","%s") on duplicate key update value="%s"' % (name,value,type(value).__name__,value)
        c.execute(sql)
        return not c.rowcount == 0

    def getAllValues(self):
        c = self.conn.cursor()
        c.execute('select name,value,type from configvalues')
        return c.fetchall()
    
    def getInterfaces(self):
        c = self.conn.cursor()
        c.execute('select * from interfaces')
        tmp = []
        for r in c:
            tmp.append(r)
        return tmp

    def setInterface(self, interfaceid, interface, nickname, argument):
        c = self.conn.cursor()
        sql = 'insert into interfaces (interfaceid, name, arguments, nickname) values(%s,"%s","%s","%s") on duplicate key update name="%s", arguments="%s", nickname="%s"' % (interfaceid, interface, argument, nickname, interface, argument, nickname)
        c.execute(sql)
        return not c.rowcount == 0

    def setIOBinding(self, publicaddress, name, interface, address):
        c = self.conn.cursor()
        sql = 'insert into IObindings (publicaddress, interfaceid, privateaddress, nickname) values(%s,%s, "%s", "%s") on duplicate key update interfaceid=%s, privateaddress="%s", nickname="%s"' % (publicaddress,interface, address, name, interface, address, name)
        c.execute(sql)
        return not c.rowcount == 0

    def getInterfaceInfoFromId(self, i):
        c = self.conn.cursor()
        c.execute('select * from interfaces where interfaceid=%s' % i)
        return c.fetchone()

    def getIOBindings(self):
        c = self.conn.cursor()
        c.execute('select * from IObindings')
        return c.fetchall()

    def getInfoFromAddress(self, addr):
        c = self.conn.cursor()
        if type(addr) is str:
            c.execute('select interfaceid, privateaddress from IObindings where nickname="%s"' % addr);
        else:
            c.execute('select interfaceid. privateaddress from IObindings wher publicaddress=%i' % addr)
            
        ret = c.fetchone()
        if ret == None or len(ret) == 0:
            raise Exception("Specified address (%s) don't exist" % addr)
        else:
            return ret
