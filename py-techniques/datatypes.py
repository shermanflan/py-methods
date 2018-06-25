# Python is strongly typed (types do not change).

# Integer division
a = 11
b = 2

print(a // 2) # prints 5 (throws away remainder)
print(a / 2) # prints 5.5 (keeps remainder)

# Other math
print (a ** b) # power
print (divmod(a, b)) # produce quotient and remainder

# Number literals
base10 = 10
base2 = 0b10
base8 = 0o10
base16 = 0x10

print(base10)
print(base2)
print(base8)
print(base16)

# Type conversion
print(int(True))
print(int(False))
print(int(3.5))
print(int('100'))
print(float('100.05'))
print(float('10e5'))
print(str(10))
print(str(10e4))

# Strings are immutable
text = 'Hello\n' + ('World!' * 2)
multi = '''Hello
World Again!''' + text[1] + text[-1]

print(text)
print(len(text))
print(multi)

list = ['c', 'a', 't']

# Slicing
text2 = "abcdefghijklmnopqrstuvwxyz"

print(text2[:]) # entire string
print(text2[5:]) # Postion 5 to the end 
print(text2[-5:]) # 5 from the end to the end
print(text2[5:-5]) # Postion 5 to 5 from the end 
print(text2[:5]) # beginning to position 5
print(text2[0:10:2]) # Skip 2 
print(text2[-1::-1]) # Reverse
print(text2[::-1]) # Reverse

# String functions
print(multi.split(' '))
print(','.join(list))
print(text2.startswith('abc'))
print(text2.endswith('xyz'))
print(text2.find('jkl'))
print(text2.rfind('stu'))
print(text2.count('k'))
print(text2.isalnum())
print(text2.strip('a'))
print(text2.capitalize())
print(text2.title())
print(text2.upper())
print(text2.swapcase())
print(text2.replace('a', 'tmp'))
print(text2.replace('a', 'tmp', 100))