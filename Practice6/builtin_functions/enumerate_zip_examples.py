names = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 88]

print("Using enumerate:")
for i, name in enumerate(names):
    print(i, name)

print("Using zip:")
for name, score in zip(names, scores):
    print(name, score)