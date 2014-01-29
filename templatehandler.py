import re

class Template(object):
    def __init__(self, templatepath):
        self.templateContents = open(templatepath,"r").read()
        self.settedKeys = {}

    def setKey(self, key, value, append=False):
        if append:
            self.settedKeys[key] += value
        else:
            self.settedKeys[key] = value

    def extractor(self, what, fromwhat):
        matches = re.findall("\[%s\](.*?)\[/%s\]" % (what,what),fromwhat, re.S)
        if len(matches) > 0:
            return matches[0]
        else:
            return ""

    def extractIterator(self,text):
        matches = re.findall("\[ITER=([0-9]+)\](.*?)\[/ITER\]", text, re.S)
        if len(matches) > 1:
            return [matches[0],matches[1]]
        else:
            return [1,""]

    def setKeyFromArr(self, key, arr):
        matches = re.findall("<!--\[%s\](.*?)-->" % key, self.templateContents, re.S)
        if matches[0] != "":
            head = self.extractor("HEADER", matches[0])
            item = self.extractor("ITEM", matches[0])
            foot = self.extractor("FOOTER", matches[0])
            iterdata = self.extractIterator(matches[0])
            tmp = head
            for i,v in enumerate(arr):
                tmp += item
                for keys in v:
                    values = str(v[keys])
                    tmp = tmp.replace("[%s]" % keys,values)

                if (i+1) % iterdata[0] == 0:
                    tmp += iterdata[1]

            tmp += foot
            self.setKey(key, tmp)


    def getRendered(self):
        tmp = self.templateContents
        for key in self.settedKeys:
            value = self.settedKeys[key]
            reg = re.compile("<!--\[%s\](.*?)-->" % key, re.S)
            tmp = re.sub(reg, value ,tmp)
            
        return tmp
