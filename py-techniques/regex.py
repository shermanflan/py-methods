import re

'''
https://docs.python.org/3.6/howto/regex.html#regex-howto
'''

# Parse a float
# 'r' removes need for slash escapes
# """ allows multiline strings
exp = r"""[+-]?\d*\.\d+""" 
p = re.compile(exp, re.IGNORECASE | re.VERBOSE) # VERBOSE allows whitespace and comments '#'

num = '+1.25'
m = p.match(num) # returns match object

if m:
    print(f'Match found: {m.group()}') # the string matched
    print(m.start())
    print(m.end())
    print(m.span()) # start plus end
else:
    print('No match')

# Inline option
if re.match(exp, num, re.IGNORECASE): # also returns match object
    print(f'Match found inline')

# Repeater alphanum
S = '__commit__'
rex = r""".*?([a-zA-Z0-9])\1.*?"""

p = re.compile(rex, re.VERBOSE)

m = p.match(S)

if m:
    print('Repeater: {0}'.format(m.groups()))
    print('Repeater: {0}'.format(m.group()))
    print('Repeater: {0}'.format(m.group(1)))
else:
    print('Repeater no match')

# Overlapping match via + look-ahead assertion
S = 'abaabaabaabaae'

pat = r"""  (?=
            [QWRTYPSDFGHJKLZXCVBNM]
            ([AEIOU]{2,})
            [QWRTYPSDFGHJKLZXCVBNM]
            )"""
p = re.compile(pat, re.IGNORECASE | re.VERBOSE)
matches = p.findall(S)

if matches:
    print('\n'.join(matches))
else:
    print(-1)

# Password complexity!!!
rex = r""" (?!.*(.).*\1) # -lookahead no dups
           (?=(.*[0-9]){3,}) # +lookahead at least 3 digits
           (?=(.*[A-Z]){2,}) # +lookahead at least 2 uppers
           [a-zA-Z0-9]{10} # exactly 10 alphanums
          """
p = re.compile(rex, re.VERBOSE)

m = p.match('B1CD102354')
if m:
    print('Valid password')
else:
    print('Invalid password')

# Substitution
s = """AAABCCDDDD"""
nn2 = r"""(?P<twoplus>(?P<single>[a-zA-Z])(?P=single){1,})"""
re_nn2 = re.compile(nn2, flags=0)
matched = re_nn2.finditer(s)

for m in matched:
    print(m)
    print(m.group("single"))
    print(m.start("twoplus"), m.end("twoplus"))
    print(m.span("twoplus"))

compressed = re_nn2.sub(lambda m: m.group("single")+str(len(m.group("twoplus"))), s)
print(f'Sub: {compressed}')

