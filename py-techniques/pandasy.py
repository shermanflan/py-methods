import numpy as np
import pandas as pd

# Series: 1-d array
obj = pd.Series([4, 7, -5, 3], index=['Col1', 'Col2', 'Col3', 'Col4'])
print(f'{obj}')
print(f'{obj.index}, {obj.values}')

obj['Col1'] = 21
obj['Col2'] = 21
print(f"{obj['Col1']}")
print(f"{obj[['Col1', 'Col2']]}")

obj2 = obj[obj > 10]
print(f'Filtered: \n{obj2}')

obj3 = obj * 3
print(f'Scalar *: \n{obj3}')

# Like a dict
if 'Col1' in obj:
    print(f'Col1 exists.')

# Load from a dict
sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000, 'California': None}
obj4 = pd.Series(sdata)
print(f"4: {obj4}")

# Check for Null - inverse is notnull()
if obj4.isnull().any():
    print(f"{obj4.isnull()}")

sdata2 = {'Ohio': 1, 'Texas': 1, 'California': 99000}
obj5 = pd.Series(sdata2)
obj5.name = 'Addition'
obj5.index.name = 'States'

# Addition: None + anything = None
print(f"5: {obj5}")
print(f"Add: \n{obj4 + obj5}")

# Alter index names:
obj5.index = ['State1', 'State2', 'State3']
print(f"5: {obj5}")

# Re-index with forward fill
obj6 = pd.Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])

print(f"df6\n{obj6.reindex(range(6), method='ffill')}") # also bfill

# Drop index values
obj6 = pd.Series(np.arange(5.), index=['a', 'b', 'c', 'd', 'e'])
obj7 = obj6.drop(['d', 'c'])
print(f"7:\n{obj7}")

# Accessing
obj8 = pd.Series(np.arange(4.), index=['a', 'b', 'c', 'd'])
print(f"8:\n{obj8['b']} = {obj8[1]}")
print(f"8b:\n{obj8[2:4]}\n{obj8[['b', 'a', 'd']]}")
print(f"8c:\n{obj8[obj8 < 2]}") # predicate
print(f"8d:\n{obj8['b':'c']}") # slicing with labels is inclusive

# Setting
obj8['b':'c'] = 5 # also inclusive
print(f"8e:\n{obj8}")

# Arithmetic
s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=['a', 'c', 'd', 'e'])
s2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1], index=['a', 'c', 'e', 'f', 'g'])
print(f"Add:\n{s1 + s2}") # introduces missing values in the label locations that don’t overlap

# Sorting, NaN sorted last
obj9 = pd.Series(range(4), index=['d', 'a', 'b', 'c'])
print(f"Sort:\n{obj9.sort_index()}") # by index
print(f"Sort2:\n{obj9.sort_values()}") # by value

# Ranking, optional 'ascending=False'
obj10 = pd.Series([7, -5, 7, 4, 2, 0, 4])
print(f"Rank:\n{obj10.rank()}")
print(f"Rank2:\n{obj10.rank(method='first')}") # ties broken by physical order
print(f"Rank3:\n{obj10.rank(method='max')}") # ties assigned same value, like SQL Rank()

# Duplicate index labels
obj11 = pd.Series(range(5), index=['a', 'a', 'b', 'b', 'c'])

if not obj11.index.is_unique:
    print(f"{obj11['a']}!") # returns all elements matching index