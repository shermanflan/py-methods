import re

#m = re.match(r'(\w+)@(\w+)\.(\w+)','username@hackerrank.com')
#m.group(0)       # The entire match 
#m.group(1)       # The first parentesized subgroup.
#m.group(2)       # The second parenthesized subgroup.
#m.group(3)       # The third parenthesized subgroup.
#m.group(1,2,3)   # Multiple arguments give us a tuple.
#m.groups() # same
#
#m2 = re.match(r'(?P<user>\w+)@(?P<website>\w+)\.(?P<extension>\w+)','myname@hackerrank.com')
#m2.groupdict()
#s = '0'
#if not bool(re.match('[+-.\d]', s)):
#    print(False)
#elif not bool(re.search('.\d', s)):
#    print(False)


import re
pattern = r'(?=(aa))'
m = re.findall(pattern, 'baaadaab')
#m = re.findall(pattern, 'rabaaacdeefgyYhFjkIoomnpOeorteeeeet')

print(m)
#print(m.groups())

#if len(m.groups()) > 0:
#    print(m.group(1))
#else:
#    print(-1)