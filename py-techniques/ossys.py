
with open('data\oops.txt', 'wt') as fout:
    print('Oops, I created a file.', file=fout)
    fout.write('Another line.')

import os

name = 'data\oops.txt'

print(os.path.exists('data\oops.txt'))
print(os.path.exists('./oops.txt'))
print(os.path.exists('waffles'))
print(os.path.exists('.'))
print(os.path.exists('..'))

print(os.path.isfile('data\oops.txt'))
os.path.isdir(name)

print(os.path.isabs(name)) # check is absolute path

# Copy
import shutil

shutil.copy(name, 'data\ohno.txt')

try:
    shutil.move(name, 'data\ohno.txt')
    os.rename('data\ohno.txt', 'data\ohwell.txt')
    os.link('data\ohwell.txt', 'data\yikes.txt')
    print(os.path.isfile('data\yikes.txt'))
except Exception as e:
    print(e)

print(os.path.islink('data\yikes.txt'))

print(os.path.abspath('data\ohno.txt'))
os.remove('data\ohno.txt')
print(os.path.exists('data\ohno.txt'))

# Directories
try:
    os.mkdir('data\poems')
    os.mkdir('data\poems\mcintyre')
    print(os.path.exists('data\poems'))
    print(os.listdir('data\poems'))
except FileExistsError as e:
    print(e)

os.chdir('data')
print(os.listdir('.'))
os.chdir('..')

os.rmdir('data\poems\mcintyre')
os.rmdir('data\poems')
print(os.path.exists('data\poems\mcintyre'))

# Simple pattern matching
import glob

# * matches everything (re would expect .*)
# ? matches a single character
# [abc] matches character a, b, or c
# [!abc] matches any character except a, b, or c
print(glob.glob('m*'))

# Processes
print(os.getpid())
print(os.getcwd())

import subprocess

ret = subprocess.getoutput('dir p*')
print(ret)

ret = subprocess.getstatusoutput('dir p*')
print(ret)

# Dates/Calendar
import calendar

print(calendar.isleap(1900))

from datetime import date

halloween = date(2014, 10, 31)

print(halloween)
print(halloween.isoformat())

print(halloween.day)
print(halloween.month)
print(halloween.year)

now = date.today()
print(now)

import locale

print('Locale: {0}'.format(locale.locale_alias.keys()))

try:
    for lang_country in ['en_us', 'fr_fr', 'de_de', 'es_es', 'is_is',]:
        locale.setlocale(locale.LC_TIME, lang_country)
        print(halloween.strftime('%A, %B %d'))
except locale.Error as e:
    print(e)

from datetime import timedelta

one_day = timedelta(days=1)
tomorrow = now + one_day
print(tomorrow)
print(now + 17*one_day)

yesterday = now - one_day
print(yesterday)

from datetime import time
noon = time(12, 0, 0)
print(noon)

print(noon.hour)
print(noon.minute)
print(noon.second)
print(noon.microsecond)

from datetime import datetime

some_day = datetime(2014, 1, 2, 3, 4, 5, 6)
print(some_day)
print(some_day.isoformat())

now = datetime.now()
print(now)

print(now.month)
print(now.day)
print(now.hour)
print(now.minute)
print(now.second)
print(now.microsecond)

noon = time(12)
this_day = date.today()
noon_today = datetime.combine(this_day, noon)
print(noon_today)
print(noon_today.date())
print(noon_today.time())

import time as tm

now = tm.time()
print(now) # epoch - sec since 1970-01-01
print(tm.ctime(now))
print(tm.localtime(now))
print(tm.gmtime(now))

t = tm.localtime(now)
print(tm.mktime(t))

fmt = "It's %A, %B %d, %Y, local time %I:%M:%S%p"
t = tm.localtime()
print(t)
print(tm.strftime(fmt, t))

fmt = "%Y-%m-%d"
print(tm.strptime("2012-01-29", fmt))