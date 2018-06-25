from collections import namedtuple

# Lists are mutable
empty = []
empty2 = list()
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
catlist = list('cat')

days[0] = 'lunes'
print(days[0])
print(days[-1])
print(days[0:7:2])

daysdays = [days, days]
daysdays.insert(0, 'january')
daysdays.append(['may'])
daysdays.extend(['june', 'july']) # combines
daysdays += ['august', 'september'] # like extend

del daysdays[2]
del daysdays[-1]
daysdays.remove('july')

print(daysdays[1][-1]) # last element of first list
print(daysdays.pop()) # pop tail
print(daysdays.pop(0)) # pop head
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
tuple1 = ('ready', 'aim', 'fire')
toList = list(tuple1)

x, y, z = tuple1 # multiple assign
print(z)

x, y = y, x # exchange
print(x)

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

fruit.clear()

# Set (dictionary without values)
empty_set = set()
evens = {2, 4, 6, 8, 20}
odds = {1, 3, 5, 7, 9}

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
