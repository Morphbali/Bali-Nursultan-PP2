class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    def area(self):
        return self.length * self.width

l, w = map(int, input().split())
r = Rectangle(l, w)
print(r.area())
