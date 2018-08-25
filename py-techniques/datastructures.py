from collections import namedtuple

# Lists are mutable
# Deleting objects from the middle of a Python list is costly. 
# Deleting from the end of a list takes constant time, though. 
# You can delete in constant time by overwriting it with the 
# one that is currently last in the list, before calling the 
# pop method. Same condsiderations for insert/append
anything = ['spam', 2.0, 5, [10, 20]]

t = ['a', 'b', 'c', 'd', 'e', 'f']
t[1:3] = ['x', 'y'] # slice assignment does not have to be equal (list will grow/shrink)

empty = []
empty2 = list()
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
catlist = list('cat')

nums = ['1', '2', '3', '4']
print(list(map(int, nums))) # cast one liner

days[0] = 'lunes'
print(days[0])
print(days[-1])
print(days[0:7:2])

daysdays = [days, days]
daysdays.insert(0, 'january') # slower than append (b/c data movement / O(n**2) )
daysdays.append(['may']) # modifies source list, + creates new list / O(n)
daysdays.extend(['june', 'july']) # combines -- faster than sum(lists, [])
daysdays += ['august', 'september'] # like extend

del daysdays[2] # also works for slices
del daysdays[-1]
daysdays.remove('july')

print(daysdays[1][-1]) # last element of first list
print(daysdays.pop()) # pop tail
print(daysdays.pop(0)) # pop head, or 0..N
print(daysdays)
print(daysdays.index('june'))
print('june' in daysdays)
print(daysdays.count('june'))
print(','.join(daysdays[0]))
print(sorted(daysdays[0])) # returns new list
daysdays[0].sort(reverse=True) # sorts in place
print(daysdays[0])

newlist = daysdays[0].copy()
newlist2 = list(daysdays[0])
newlist3 = daysdays[0][:]
daysdays[0][6] = 'viernes'
print(daysdays[0])
print(newlist3)

# Tuples are immutable (constant list)
t0 = ('a',) # comma required for tuple, otherwise a string
print(type(t0))
tuple1 = ('ready', 'aim', 'fire')
toList = list(tuple1)
quot, rem = divmod(7, 3)

x, y, z = tuple1 # multiple assign
print(z)

x, y = y, x # exchange
print(x)

for index, element in enumerate('abc'):
    print(index, element)

# Named tuples (like structs)
Duck = namedtuple('duck', 'bill tail')
parts = {'bill': 'wide orange', 'tail': 'long'}
daffy = Duck(**parts) # keyword argument shorthand
print(daffy.bill)
print(daffy.tail)

# Immutable
duck3 = daffy._replace(tail='magnificent', bill='crushing')
print(duck3.bill)
print(duck3.tail)

# Dictionary!
empty_dict = {}
fruit = {
    'apple': 'red',
    'banana': 'yellow',
    'orange': 'orange',
    }

list = [['test', 1], ['test2', 2], ['test3', 3]]
dict2 = dict(list)
dict2['test'] = 21
dict2['newkey'] = 22

list2 = [['test4', 4], ['test5', 5]]

dict3 = dict2.copy() # new copy

dict2.update(list2) # merge dictionaries
del fruit["apple"]

print(fruit)
print(dict2)
print(dict3)
print(dict2.keys()) # returns enumerable
print(dict2.values()) # returns enumerable
print(dict2.items()) # returns enumerable of tuples
print("apple" in fruit)
print(fruit.get('kiwi', "Does not exist!"))

d = dict(zip('abc', range(3)))
print(d)

fruit.clear()

# Ordered dictionary
# keeps track of the order in which its keys were inserted.

a = OrderedDict()
a['foo'] = 1
a['bar'] = 2

b = OrderedDict()
b['foo'] = 'red'
b['bar'] = 'blue'

for value1, value2 in zip(a.values(), b.values()):
    print(value1, value2)

# Default Dict automatically stores a default value when a key doesn’t exist.
stats = defaultdict(int) # passed in function returns default
stats['my_counter'] += 1

# Set (dictionary without values)
# Membership checks are linear for lists and constant for sets.
empty_set = set()
evens = {2, 4, 6, 8, 20}
odds = {1, 3, 5, 7, 9}
odds.add(7)

print(evens)
print(odds)
print(set('apple'))
print(set(['one', 'one', 'one']))
print(set(('one', 'one', 'one')))
print(set(dict3)) # ignores values
print(3 in evens)
print(evens & odds) # intersect
print(evens | odds) # union
print(evens - odds) # except
print(evens ^ odds) # xor
print(evens <= odds) # subset
print(evens < odds) # proper subset

# Deque
# Constant time operations for inserting or removing items from its beginning or end
from collections import deque

fifo = deque()
fifo.append(1)      # Producer
x = fifo.popleft()  # Consumer

d = deque(['6', '9', '8', '7', '3'])
d.rotate(3)
print(d)

# Counter
from collections import Counter

# Like { c: s.count(c) for c in s }
c = Counter('amanaplanacanalpanama')

for k, v in c.items():
    print(k, v)

# Priority Queue
import heapq

a = []
heapq.heappush(a, 5)
heapq.heappush(a, 3)
heapq.heappush(a, 7)
heapq.heappush(a, 4)

print(a[0])
print(heapq.heappop(a), heapq.heappop(a), heapq.heappop(a), heapq.heappop(a))