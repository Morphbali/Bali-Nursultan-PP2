class StringHandler:
    def getString(self):
        self.s = input()
    def printString(self):
        print(self.s.upper())

h = StringHandler()
h.getString()
h.printString()
