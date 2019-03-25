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
