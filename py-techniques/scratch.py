def unicode_test(value):
    import unicodedata
    name = unicodedata.name(value)
    value2 = unicodedata.lookup(name)
    print('value="%s", name="%s", value2="%s"' % (value, name, value2))

mystery = '\U0001f4a9'

print('{0}'.format(mystery))

unicode_test(mystery)

pop_bytes = mystery.encode('utf-8')

print(pop_bytes)

print(pop_bytes.decode('utf-8'))

letter = '''Dear {salutation} {name},
Sincerely,
{spokesman}
{job_title}'''

print(letter.format(salutation='Mr.', name='Ricardo', spokesman='John Smith', job_title='CEO'))

mammoth = '''We have seen thee, queen of cheese,
Lying quietly at your ease,
Gently fanned by evening breeze,
Thy fair form no flies dare seize.
All gaily dressed soon you'll go
To the great Provincial show,
To be admired by many a beau
In the city of Toronto.
Cows numerous as a swarm of bees,
Or as the leaves upon the trees,
It did require to make thee please,
And stand unrivalled, queen of cheese.
May you not receive a scar as
We have heard that Mr. Harris
Intends to send you off as far as
The great world's show at Paris.
Of the youth beware of these,
For some of them might rudely squeeze
And bite your cheek, then songs or glees
We could not sing, oh! queen of cheese.
We'rt thou suspended from balloon,
You'd cast a shade even at noon,
Folks would think it was the moon
About to fall and crush them soon.'''

import re

r = re.findall(r'\bc\w*', mammoth)
r = re.findall(r'\bc\w{3}\b', mammoth)
r = re.findall(r'\w*r\b', mammoth)
r = re.findall(r'\w*[aeiou]{3}\w*', mammoth)
print(r)