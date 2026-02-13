class A:
    def hello(self):
        print("Hello from A")

class B:
    def hi(self):
        print("Hi from B")

class C(A, B):
    pass

c = C()
c.hello()
c.hi()
