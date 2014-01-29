from templatehandler import Template
import config, xmlrpclib


def run(query):
    maintempl = Template("webadmintemplate.templ")
    subtempl = Template("adminutilities.templ")
    conf = config.Config()

    if query.has_key("xmlrpcok") and query.has_key("xmlrpccommand"):
        port = conf.getValue("xmlport")
        subtempl.setKey("xml_msg", "<font style=\"color:green;\">XML-PRC Command was send sucessfully</font><br>")
        subtempl.setKey("prevcommand", query["xmlrpccommand"])
    else:
        subtempl.setKey("prevcommand", "")
        subtempl.setKey("xml_msg", "")


    maintempl.setKey("contents", subtempl.getRendered())
    return maintempl.getRendered()
