from modulewrapper import ModuleBase

class module(ModuleBase):
    def __init__(self, mao):
        ModuleBase.__init__(self)
        mao.Network.register_function(self.printer, "printer")
        mao.Network.register_function(self.hi, "hi")
        mao.HAL.register_event("StairLight", self.testregister, ["a","b",1])

    def hi(self):
        return "Hello"

    def testregister(self, a, b, c):
        print a,b,c

    def run(self, mao):
        pass

    def printer(self, text):
        print text
        return True
