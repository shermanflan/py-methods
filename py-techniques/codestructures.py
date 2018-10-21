# Flow control
disastertype = 'tornado'

if disastertype == 'earthquake':
    print('woah!')
elif disastertype == 'hurricane':
    print('nooo!')
else:
    print('oh no!')

# Ternary if (in-line)
my_values = { 'red': ['7'], 'blue': [0], 'green': [3] }
red = my_values.get('red', [''])
red = int(red[0]) if red[0] else 0
print(red)

# Looping
count = 1

#while count > 0:
#    stuff = input('String to capitalize [q to quit]: ')
#
#    if stuff == 'q':
#        break; # continue also supported
#
#    print(stuff.upper())
#    count += 1

rabbits = ['tom', 'bugs', 'roger', 'jerry']

for name in rabbits:
    print(name)

word = 'mississippi'

for c in word:
    print(c)

authors = {
        'king': ['It', 'Christine', 'The Shining'],
        'card': ['Ender''s Game', 'Speaker for the Dead'],
        'heinlein': ['Stranger in a Strange Land', 'Starship Troopers']
    }

for author in authors:
    print(author)

for books in authors.values():
    print(books)

for author, books in authors.items(): # tuple assignment
    print(author, books)

indexes = [1, 2, 3]
values = ['one', 'two', 'three']

for index, value in zip(indexes, values):
    print(index, value)

print(list(zip(indexes, values))) # list of tuples
print(dict(zip(indexes, values))) # dictionary

for n in range(0, 10, 2): # slice
    print(n)

# Use enumerate over range when scanning a list:
flavor_list = ['one', 'two', 'three']
for i, flavor in enumerate(flavor_list):
    print('%d: %s' % (i + 1, flavor))

# Comprehensions
numbers = [n for n in range(0, 11, 2)] # kind of like math set notation 
odds = [n + 1 for n in range(0, 11, 2)]
odds2 = [n for n in range(0, 51) if n % 2 == 1]
xy = [(x, y) for x in range(1, 5) if x % 2 == 0 for y in range(1, 5) if y % 2 == 1] # cartesian product (l to r)

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row] # l to r, row then element
print(flat)

squared = [[x**2 for x in row] for row in matrix] # square a matrix
print(squared)

print(numbers)
print(odds)
print(odds2)
print(xy)

word = 'hello world!!!'
letter_counts = {letter: word.count(letter) for letter in set(word)}
letter_index = {letter: word.index(letter) for letter in set(word)}

print(letter_counts)
print(letter_index)

set1 = {n for n in range(1, 10, 3)}

print(set1)

# Generator comprehensions (like an enumerator)
# More memory efficient than comprehensions (like a stream)
nums = (n for n in range(0, 10))

print(nums)

for n in nums: # enumerate
    print(n)

print(list(nums)) # empty (implicitly iterates)

# Functions!

def myFirstFun(anything = 'default value'):
    return 'Hello World!' + anything

print(myFirstFun(anything = '!!!'))

def printArgs(*args):
    print(args)

def log(message, *values):  # any number of args after the first
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

def printArgsKV(**args): # create dictionary
    print(args)

# * indicates the end of positional arguments and the beginning of keyword-only arguments
def safe_division_c(number, divisor, *,
                    ignore_overflow=False,
                    ignore_zero_division=False):
    pass

printArgs('1', '2', '3')

l = ['1', '2', '3', '4']
printArgs(*l) # scatters list into arguments

printArgsKV(key1='val1', key2='val2', key3='val3')

def times3(*args):
    return sum(args)

def invoke(func, *args): # function delegate
    print(func(*args))

invoke(times3, 1, 2, 3, 4, 5)

def outer(a, b):
    def inner(c, d):
        return c - d
    return a + b + inner(a, b)

print(outer(1, 2))

def returnClosure(str1):
    'Returns a closure: function'
    def inner():
        print("The arg is: %s" % str1)

    return inner

func1 = returnClosure("hellow")
func1()

def iterate1(words, func1):
    for w in words:
        print(func1(w))

iterate1(['a', 'nice', 'day'], lambda word: word.upper() + '!') # lambda syntax

# Generator functions / iterators
# More memory efficient than building a list and returning it.
def my_range(first, last, step):
    num = first

    while first < last:
        yield first # creates state machine
        first += step

for n in my_range(0, 10, 2):
    print(n)

# Decorator: takes a func as an arg and returns another function
def docFunc(func):
    def decorateFunc(*args, **kwargs):
        print('Running function:', func.__name__)
        print('Positional arguments:', args)
        print('Keyword arguments:', kwargs)
        result = func(*args, **kwargs)
        print('Result:', result)
        return result
    return decorateFunc

def myAdd(p, q, **kwargs):
    return p + q

newFunc = docFunc(myAdd) # manual decorator assignment
newFunc(2, 4, key1='val1', key2='val2')

# Or
# Same as: myAdd2 = docFunc(myAdd2)
@docFunc
def myAdd2(p, q, **kwargs):
    return p + q

myAdd2(4, 6, key1='val1', key2='val2')

def squareIt(func):
    def newFunction(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * result
    
    return newFunction

# Chained decorators
@docFunc
@squareIt
def myAdd3(p, q, **kwargs):
    return p + q

myAdd3(1, 2)

# Global variable scope
animal = "kitten"

def changeGlobal():
    global animal # without this variable is scoped to function
    animal = animal.upper() + '!'

print(animal)
changeGlobal()
print(animal)

def changeLocal():
    animal = 'tiger'
    print('locals: ', locals())

changeLocal()
print('globals: ', globals())

# Exception / Try Catch
try:
    mylist = [1, 2, 3]
    print(mylist[5])
except IndexError as e:
    print("Out of bounds!: ", e)
except Exception as e:
    print("Unknown: ", e)
finally:
    print('Always run this!')

mylist2 = {1, 2, 3, 4}

for n in mylist2:
    if n % 2 == 0:
        raise Exception('Even number!')

# Enums
from enum import Enum

class State(Enum):
    COMPLETE = 1
    PARTIAL = 2
    BLANK = 3

