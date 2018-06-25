snowman = '\u2603'
print(snowman)

cafe = 'caf\u00e9'
print(cafe)

# Encode to byte sequence
try:
    smbytes = snowman.encode('utf-8')

    print(smbytes)

    plbytes = cafe.encode() # default utf-8

    print(plbytes)

    cafe = plbytes.decode('utf-8') # back to string

    print(cafe)
except UnicodeEncodeError as e:
    print(e)
except UnicodeDecodeError as e:
    print(e)

# Formatting
n = 21
f = 7.0
s = 'condesa'

print('{0} {1} {2}'.format(n, f, s))
print('{0:d} {1:f} {2:s}'.format(n, f, s))
print('{0:20d} {1:20f} {2:20s}'.format(n, f, s)) # field width
print('{0:<20d} {1:<20f} {2:<20s}'.format(n, f, s)) # field width, left align
print('{0:^20d} {1:^20.2f} {2:+^20s}'.format(n, f, s)) # field width, centered, with pad

ht = {'n': 42, 'f': 7.03, 's': 'cheese'}

print('{0[n]} {0[f]} {0[s]} {1}'.format(ht, 'other')) # format dictionary vals

# Regular Expressions
import re
import string

source = 'Young Frankenstein'

#m = re.match('^You', source) # start anchor
m = re.match('.*Frank', source) 
if m:
    print(m.group())

m = re.search('Frank', source)

if m:
    print(m.group())

m = re.findall('n.?', source) # returns list

if m:
    print(m)

m = re.split(' ', source) # returns list

if m:
    print(m)

m = re.sub('n', 'N', source) # returns a string

if m:
    print(m)

printable = string.printable

print(printable)
print(re.findall('\d', printable))
print(re.findall('\w', printable))
print(re.findall('\s', printable))

source = '''I wish I may, I wish I might
Have a dish of fish tonight.'''

print(re.findall('wish|fish', source))
print(re.findall('^wish', source))
print(re.findall('fish$', source))
print(re.findall('[wf]ish', source))
print(re.findall('[wsh]+', source))
print(re.findall('ght\W', source))
print(re.findall('I (?=wish)', source))
print(re.findall('(?<=I) wish', source))
print(re.findall(r'\bfish', source))

# Bytes/Byte Arrays
blist = [1, 2, 3, 255]

the_bytes = bytes(blist) # immutable
the_byte_array = bytearray(range(0, 256)) # mutable
#the_byte_array[2] = 127

print(the_bytes)
print(the_byte_array)