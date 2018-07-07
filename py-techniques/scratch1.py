from collections import defaultdict

with open('C:/Users/rguzman/Documents/GitHub/py-methods/py-techniques/data/input.txt', 'rt') as f:
    k = f.readline()

    rooms = f.read()
    #words = f.read().split()

rooms = list(map(int, rooms.split()))
rooms.sort()
print(rooms)
prev = 0
next = 0
for i in range(1, len(rooms) - 1):
    prev = rooms[i - 1]
    next = rooms[i + 1]
    if prev != rooms[i] and rooms[i] != next:
        print(rooms[i])
        break
else:
    print(rooms[-1])