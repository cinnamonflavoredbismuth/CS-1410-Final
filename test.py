class parent:
    def __init__(self, parattr='hi'):
        self.parattr=parattr
    def go(self):
        print(self.parattr)

class child(parent):
    def __init__(self, parattr='hi',childattr='hello'):
        super().__init__(parattr)
        self.childattr=childattr
    def go(self):
        print(self.childattr)

c=child()
c.go()