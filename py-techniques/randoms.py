import random

for i in range(10):
    x = random.random()
    print(x)

print(random.randint(5, 10)) # inclusive

t = [1, 2, 3]
print(random.choice(t))