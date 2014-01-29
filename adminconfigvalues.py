import config
from templatehandler import Template

def run(query):
    conf = config.Config()
    maintempl = Template("webadmintemplate.templ")
    subtempl = Template("adminconfigvalues.templ")

    if query.has_key("ok"):
        methods = {"float": float, "int": int, "str": str}
        value = methods[query["type"]](query["value"])
        conf.setValue(query["name"], value)
    
    buff = ""

    arr = []
    for r in conf.getAllValues():
        buff = ""
        for s,f in [["int","Integer"],["float","Float"],["str","String"]]:
            if s == r[2]:
                selected = "selected"
            else:
                selected = ""
                
            buff += "<option value=\"%s\" %s>%s</option>" % (s,selected,f)

        arr.append({"name": r[0], "value": r[1], "select": buff})
        
    subtempl.setKeyFromArr("list", arr)
    maintempl.setKey("contents", subtempl.getRendered())
    return maintempl.getRendered()
