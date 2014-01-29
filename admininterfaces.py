from templatehandler import Template
import config,os

def run(query):
    maintempl = Template("webadmintemplate.templ")
    subtempl = Template("admininterfaces.templ")
    conf = config.Config()

    if query.has_key("ok"):
        conf.setInterface(query["interfaceid"], query["interface"], query["nickname"], query["argument"])

    interfacelist = getInterfaceList()
    subtempl.setKey("selectdata", "".join(["<option value=\"%s\">%s</option>" % (s,s) for s in interfacelist]))

    arr = []
    for r in conf.getInterfaces():
        buff = ""
        for s in interfacelist:
            if s == r[1]:
                selected = "selected"
            else:
                selected = ""

            buff += '<option value="%s" %s>%s</option>' % (s, selected, s)

        arr.append({"interfaceid": r[0], "selectdata": buff, "nickname": r[3], "argument": r[2]})

    subtempl.setKeyFromArr("list", arr)
    maintempl.setKey("contents", subtempl.getRendered())
    return maintempl.getRendered()

def getInterfaceList():
    retval = []
    for x in os.listdir("interfaces/"):
        if x != "." and x != ".." and x[-2:] == "py":
            retval.append(x[0:-3])
    return retval
