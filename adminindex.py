from templatehandler import Template

def run(query):
    templ = Template("webadmintemplate.templ")
    templ.setKey("contents", "<h1>Welcome</h1><i>Choose activity in the menu to the left</i>")
    return templ.getRendered()
