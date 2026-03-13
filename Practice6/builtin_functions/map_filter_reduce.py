from functools import reduce

numbers = [1, 2, 3, 4, 5]

squares = list(map(lambda x: x * x, numbers))
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
total = reduce(lambda a, b: a + b, numbers)

print("Original list:", numbers)
print("Squares:", squares)
print("Even numbers:", even_numbers)
print("Sum:", total)