poem = '''There was a young lady named Bright,
Whose speed was far faster than light;
She started one day
In a relative way,
And returned on the previous night.'''

# Write file
# r means read.
# w means write. If the file doesn’t exist, it’s created. If the file does exist, it’s overwritten.
# x means write, but only if the file does not already exist.
# a means append (write after the end) if the file exists.
# t (or nothing) means text.
# b means binary.
try:
    fout = open('data/relativity.txt', 'wt')
    fout.write(poem)
    fout.close()
except IOError as e:
    print(e)

# Write in chunks
fout = open('data/relativity.txt', 'wt')
size = len(poem)
offset = 0
chunk = 100
while True:
    if offset > size:
         break
    fout.write(poem[offset:offset+chunk])
    offset += chunk

fout.close()

# Read file
fin = open('data/relativity.txt', 'rt' )
poem = fin.read()
fin.close()
print(len(poem))

# Read in chunks
poem = ''

try:
    fin = open('data/relativity.txt', 'rt' )
    chunk = 100
    while True:
        fragment = fin.read(chunk)
        if not fragment:
            break
        poem += fragment

    fin.close()
except FileNotFoundError as e:
    print(e)

print(len(poem))

# Read lines
poem = ''
fin = open('data/relativity.txt', 'rt' )
while True:
    line = fin.readline()
    if not line:
        break
    poem += line

fin.close()
print(len(poem))

# Read via iterator
poem = ''

try:
    fin = open('data/relativity.txt', 'rt' )
    for line in fin:
        poem += line

    fin.close()
except FileNotFoundError as e:
    print(e)

print(len(poem))

# Read via readlines
fin = open('data/relativity.txt', 'rt' )
lines = fin.readlines()
fin.close()
print(len(lines), 'lines read')

for line in lines:
    print(line, end='')

# Write Binary file
bdata = bytes(range(0, 256))

fout = open('data/bfile.dat', 'wb')
fout.write(bdata)

fout.close()

# Write binary in chunks
fout = open('data/bfile.dat', 'wb')
size = len(bdata)
offset = 0
chunk = 100
while True:
    if offset > size:
         break
    fout.write(bdata[offset:offset+chunk])
    offset += chunk

fout.close()

# Binary read
fin = open('data/bfile.dat', 'rb')
bdata = fin.read()
print(len(bdata))

fin.close()

# Close files automatically (like using)
with open('data/relativity.txt', 'wt') as fout:
    fout.write(poem)

# Seek
fin = open('data/bfile.dat', 'rb')
print(fin.tell()) # get current pos
fin.seek(255) # seek to last char

bdata = fin.read()
print(len(bdata))

print(bdata[0])

# CSV!!!!!!!!!!!!!!
import csv

villains = [
    ['Doctor', 'No'],
    ['Rosa', 'Klebb'],
    ['Mister', 'Big'],
    ['Auric', 'Goldfinger'],
    ['Ernst', 'Blofeld'],
    ]

with open('data/villains.csv', 'wt') as fout:  # a context manager
    csvout = csv.writer(fout, dialect='excel')
    # TODO: Prints out extra newlines
    csvout.writerows(villains)

# Read back (list of lists)
with open('data/villains.csv', 'rt') as fin:  # context manager
    cin = csv.reader(fin)
    villains = [row for row in cin]  # This uses a list comprehension

print(villains)

# Read back (dictionary)
with open('data/villains.csv', 'rt') as fin:
    cin = csv.DictReader(fin, fieldnames=['first', 'last'])
    villains = [row for row in cin]

print(villains)

# Write from dictionary
villains = [
    {'first': 'Doctor', 'last': 'No'},
    {'first': 'Rosa', 'last': 'Klebb'},
    {'first': 'Mister', 'last': 'Big'},
    {'first': 'Auric', 'last': 'Goldfinger'},
    {'first': 'Ernst', 'last': 'Blofeld'},
    ]

with open('data/villains.csv', 'wt') as fout:
    cout = csv.DictWriter(fout, ['first', 'last'])
    cout.writeheader()

    # TODO: Prints out extra newlines
    cout.writerows(villains)

# Read back as dictionary (ignore header)
with open('data/villains.csv', 'rt') as fin:
    cin = csv.DictReader(fin)
    villains = [row for row in cin]

print(villains)

# XML
import xml.etree.ElementTree as et

tree = et.ElementTree(file='data/menu.xml')
root = tree.getroot()

print(root.tag)

for child in root:
    print('tag: {0}, attributes: {1}', (child.tag, child.attrib))

    for grandchild in child:
        print('\ttag: {0}, attributes: {1}', (grandchild.tag, grandchild.attrib))

# JSON!!!!!!!!!!!
import json

# Dictionary of Dictionaries
menu = \
{
"breakfast": {
        "hours": "7-11",
        "items": {
                "breakfast burritos": "$6.00",
                "pancakes": "$4.00"
                }
        },
"lunch" : {
        "hours": "11-3",
        "items": {
                "hamburger": "$5.00"
                }
        },
"dinner": {
        "hours": "3-10",
        "items": {
                "spaghetti": "$8.00"
                }
        }
}

# To JSON string
menu_json = json.dumps(menu)
print(menu_json)

# To object
menu2 = json.loads(menu_json)
print(menu2)

# Write date to JSON
import datetime
from time import mktime

now = datetime.datetime.utcnow()
now_str = str(now)
print(json.dumps(now_str))

# Write date to JSON as epock
now_epoch = int(mktime(now.timetuple()))
print(json.dumps(now_epoch))

# Implement date to epock converter
class DTEncoder(json.JSONEncoder):
    def default(self, obj):
        # isinstance() checks the type of obj
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        # else it's something the normal decoder knows:
        return json.JSONEncoder.default(self, obj)

print(json.dumps(now, cls=DTEncoder))

# Config files
import configparser

cfg = configparser.ConfigParser()
cfg.read('data/settings.cfg')

try:

    print(cfg['french']['greeting'])
    print(cfg['files']['bin'])

except KeyError as e:
    print(e)

