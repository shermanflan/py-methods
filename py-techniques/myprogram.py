import sys
import mymodule1 as mm
from mymodule2 import myFunc as mf
from collections import deque
import Person

# A module is just a file of python code
print("Program args: ", sys.argv)

mm.hello()
mf('test')

# Search paths for modules
for d in sys.path:
    print(d)

# A deque (deck) is a double ended queue
def ispalindrome(word):
    tmp = word.replace(' ', '', -1)

    dq = deque(tmp)

    while len(dq) > 1:
        if dq.pop() != dq.popleft():
            return False

    return True

def ispalindrome2(word):
    tmp = word.replace(' ', '', -1)
    return tmp == tmp[::-1]

print(ispalindrome("a man a plan a canal panama"))
print(ispalindrome2("a man a plan a canal panama"))

p = Person.Person('rick')

print(p.name)
print(p.Exclaim())

ec = Person.MDPerson('john', 'rrguzman@gmail.com')

print(ec.name)
print(ec.email)

try:
    print(ec.__name)
except AttributeError as e:
    print(e)

print(ec.Exclaim())

jd = Person.JDPerson('john', '5/17/1976')

print(jd.Age)

try:
    jd.Age = 21
except AttributeError as e:
    print(e)

Person.MDPerson.staticMethod()

ec2 = Person.MDPerson('john2', 'shermanflan@gmail.com')

print(ec == ec2)
print(ec2)