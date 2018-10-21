import numpy

# Arrays must be of the same type, unlike lists
a = numpy.array([1,2,3,4,5])
print(a[1])

b = numpy.array([1,2,3,4,5], float)
print(b[1])

# MD: 3 rows and 2 columns 
my_2D_array = numpy.array([[1, 2],[3, 4],[6,5]])
print(my_2D_array.shape)
print(my_2D_array)

# Functional option for change shape
c = numpy.array([1,2,3,4,5,6], float)
print(numpy.reshape(c, (2, 3)))

# Change shape (in place)
c.shape = (2, 3) # rows by cols
print(c)

# Transpose
my_array2 = numpy.array([[1,2,3],
                        [4,5,6]])
print(f'T: {numpy.transpose(my_array2)}')

# Flatten (1 dimension)
my_array3 = numpy.array([[1,2,3],
                        [4,5,6]])
print(f'F: {my_array3.flatten()}')

# Concatenate
array_1 = numpy.array([1,2,3])
array_2 = numpy.array([4,5,6])
array_3 = numpy.array([7,8,9])

print(f'Concat: {numpy.concatenate((array_1, array_2, array_3))}')

array_4 = numpy.array([[1,2,3],[0,0,0]])
array_5 = numpy.array([[0,0,0],[7,8,9]])

print(f'ConcatAxis2: {numpy.concatenate((array_4, array_5), axis = 1)}') 

# Generate zero and one arrays
#Default type is float
print(f'zero: {numpy.zeros((1,2))}')
print(f'zero: {numpy.zeros((1,2), dtype = numpy.int)}')
print(f'one: {numpy.ones((1,2))}')
print(f'one: {numpy.ones((1,2), dtype = numpy.int)}')

# Generate identity array (1 along diagonal)
#3 is for  dimension 3 X 3
print(f'Id: {numpy.identity(3)}')

# Use eye to generate an identity with 1's offset from the diagonal
# 8 X 7 Dimensional array with first upper diagonal 1.
print(f'eye: {numpy.eye(8, 7, k = 1)}')

# Array math
ma = numpy.array([1,2,3,4], float)
mb = numpy.array([5,6,7,8], float)

print(f'math: {ma + mb}')
print(f'math: {numpy.add(ma, mb)}')
print(f'math: {ma - mb}')
print(f'math: {numpy.subtract(ma, mb)}')
print(f'math: {ma * mb}')
print(f'math: {numpy.multiply(ma, mb)}')
print(f'math: {ma / mb}')
print(f'math: {numpy.divide(ma, mb)}')
print(f'math: {ma % mb}')
print(f'math: {numpy.mod(ma, mb)}')
print(f'math: {ma**mb}')
print(f'math: {numpy.power(ma, mb)}')

my_array = numpy.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
print(f'more math: {numpy.floor(my_array)}')

my_array = numpy.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
print(f'more math: {numpy.ceil(my_array)}')

my_array = numpy.array([1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9])
print(f'round nearest int: {numpy.rint(my_array)}')

# Sum/Prod/Min/Max over given axis
# Also can do mean/var/std
my_array = numpy.array([ [1, 2], [3, 4] ])

print(f'sum: {numpy.sum(my_array, axis = 0)}') # col
print(f'sum: {numpy.sum(my_array, axis = 1)}') # row
print(f'sum: {numpy.sum(my_array, axis = None)}') # both
print(f'sum: {numpy.sum(my_array)}') # both

my_array = numpy.array([ [1, 2], [3, 4] ])

print(f'prod: {numpy.prod(my_array, axis = 0)}')
print(f'prod: {numpy.prod(my_array, axis = 1)}')
print(f'prod: {numpy.prod(my_array, axis = None)}')
print(f'prod: {numpy.prod(my_array)}')

my_array = numpy.array([[2, 5], 
                        [3, 7],
                        [1, 3],
                        [4, 0]])

print(f'min: {numpy.min(my_array, axis = 0)}')         #Output : [1 0]
print(f'min: {numpy.min(my_array, axis = 1)}')         #Output : [2 3 1 0]
print(f'min: {numpy.min(my_array, axis = None)}')      #Output : 0
print(f'min: {numpy.min(my_array)}')                   #Output : 0
print(f'max: {numpy.max(my_array, axis = 0)}')         #Output : [4 7]
print(f'max: {numpy.max(my_array, axis = 1)}')         #Output : [5 7 3 4]
print(f'max: {numpy.max(my_array, axis = None)}')      #Output : 7
print(f'max: {numpy.max(my_array)}')                   #Output : 7

# Use dot to multiply two matrices
A = numpy.array([ 1, 2 ])
B = numpy.array([ 3, 4 ])

print(f'dot: {numpy.dot(A, B)}')       #Output : 11