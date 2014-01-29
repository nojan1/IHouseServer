from templatehandler import Template
import config

def run(query):
    maintempl = Template("webadmintemplate.templ")
    subtempl = Template("adminiobindingstempl.templ")
    conf = config.Config()

    if query.has_key("ok"):
        conf.setIOBinding(query["pubaddr"],query["nickname"], query["interface"], query["address"])       

    selectdata = "".join(["<option value=\"%s\">%s</option>" % (r[0],r[3]) for r in conf.getInterfaces()])
    subtempl.setKey("selectdata", selectdata)

    arr = []
    for r in conf.getIOBindings():
        buff = ""
        selected = ""
        for i in conf.getInterfaces():
            if int(i[0]) == int(r[1]):
                selected = "selected"
            else:
                selected = ""

            buff += '<option value="%s" %s>%s</option>' % (i[0], selected, i[3])

        arr.append({"nickname": str(r[3]), "selectdata": str(buff), "address": r[2], "publicaddress": r[0]})

    
    subtempl.setKeyFromArr("list", arr)
    maintempl.setKey("contents", subtempl.getRendered())
    return maintempl.getRendered()
