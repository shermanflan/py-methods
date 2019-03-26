import numpy as np
import pandas as pd

# Dataframe: a dict of Series all sharing the same index.
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada', 'Nevada', 'Texas'],
        'year': [2000, 2001, 2002, 2001, 2002, 2003, 2004],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9, 3.2, 2.1]}
frame1 = pd.DataFrame(data)
print(f"F1\n{frame1}")

# Specify columns
frame2 = pd.DataFrame(data, columns=['state', 'year', 'pop', 'newcol']) 
print(f"F2\n{frame2.columns}")

# Update column - assigns to whole column
frame2['year'] = 2019
val = pd.Series([-1.2, -1.5, -1.7], index=[2, 4, 5])
frame2['newcol'] = val

# Access column
print(f"F2C\n{frame2['state']}")
print(f"F2C\n{frame2.year}")
print(f"F2C\n{frame2.newcol}")

# Add new column
frame2['IsTx'] = frame2.state == 'Texas'

print(f"F2\n{frame2}")

# Remove column
del frame2['IsTx']

# Initialize from a dict (cols) of dicts (rows).
pop = {'Nevada': {2001: 2.4, 2002: 2.9}, 'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
frame3 = pd.DataFrame(pop)
print(f"F3\n{frame3}")

# Transpose/Pivot
print(f"F3P\n{frame3.T}")

# Initialize from a dict (cols) of series (rows).
pdata3 = {'Ohio': frame3['Ohio'][:-1], 'Nevada': frame3['Nevada'][:2]}
frame4 = pd.DataFrame(pdata3)
frame4.index.name = 'year'
frame4.columns.name = 'state'
print(f"F4\n {frame4}")

# Check column exists
if not 'Texas' in frame4.columns:
    print(f"Column Texas not found")
    
# Access values only (ndarray)
print(f"F4V\n {frame4.values}")

# Access row
print(f"F2R\n{frame2.loc[6]}")

# Re-index
frame5 = pd.DataFrame(np.arange(9).reshape((3, 3)), index=['a', 'c', 'd'], columns=['Ohio', 'Texas', 'California'])
frame6 = frame5.reindex(['a', 'b', 'c', 'd']) # adds 'b'
states = ['Texas', 'Utah', 'California'] # adds 'Utah'
frame7 = frame6.reindex(columns=states)
print(f"7\n{frame7}")

# Drop index values, can also use argument 'inplace=True'
frame8 = pd.DataFrame(np.arange(16).reshape((4, 4)), index=['Ohio', 'Colorado', 'Utah', 'New York'], columns=['one', 'two', 'three', 'four'])
print(f"df8r\n{frame8.drop(['Colorado', 'Ohio'])}") # drop rows
print(f"df8c\n{frame8.drop(['two', 'four'], axis='columns')}") # drop cols

# Access: The row selection syntax [:2] is provided as a convenience. 
# Passing a single element or a list to the [] operator selects columns.
# Accessing columns
print(f"df8e\n{frame8['two']}")
print(f"df8e\n{frame8[['two', 'three']]}")

# Slicing rows
print(f"df8f\n{frame8[:2]}")

# Using a predicate on column 'three'
print(f"df8g\n{frame8[frame8['three'] > 5]}")

# Using a predicate on all values (returns True or False)
print(f"df8h\n{frame8 < 5}")

# Using a predicate to set values
frame8[frame8 < 5] = 0
print(f"df8i\n{frame8}")

# Selection using LOC (by label), ILOC (by integer)
print(f"df8j\n{frame8.loc['Colorado', ['two', 'three']]}") # 1 col, 2 rows
print(f"df8k\n{frame8.iloc[1, [1, 2]]}") # equivalent
print(f"df8l\n{frame8.iloc[2]}") # single col
print(f"df8l\n{frame8.iloc[[1, 2], [3, 0, 1]]}") # multi-column, multi-row
print(f"df8m\n{frame8.loc[:'Utah', 'two']}") # slicing rows, single column
print(f"df8m\n{frame8.iloc[:, :3][frame8.three > 5]}") # slicing rows and cols, then predicate selection

# Arithmetic
df9 = pd.DataFrame(np.arange(9.).reshape((3, 3)), columns=list('bcd'), index=['Ohio', 'Texas', 'Colorado'])
df10 = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns=list('bde'), index=['Utah', 'Ohio', 'Texas', 'Oregon'])
print(f"Add\n{df9 + df10}") # rows or columns that don't align are empty

# Arithmetic + fill
df11 = pd.DataFrame(np.arange(12.).reshape((3, 4)), columns=list('abcd'))
df12 = pd.DataFrame(np.arange(20.).reshape((4, 5)), columns=list('abcde'))
df12.loc[1, 'b'] = np.nan
print(f"Add2\n{df11 + df12}") # rows or columns that don't align are empty
print(f"Add3\n{df11.add(df12, fill_value=0)}") # rows or columns that don't align are filled with defaults

# Operations between dataframe and series (broadcasting)
df13 = pd.DataFrame(np.arange(12.).reshape((4, 3)), columns=list('bde'), index=['Utah', 'Ohio', 'Texas', 'Oregon'])
row1 = df13.iloc[0] # Utah
print(f"Broadcast1\n{df13 - row1}") # applied to each row

row2 = pd.Series(range(3), index=['b', 'e', 'f'])
print(f"Broadcast2\n{df13 + row2}") # rows, cols that don't align are unioned

# Broadcast on column
row3 = df13['d']
print(f"Broadcast3\n{df13.sub(row3, axis='index')}")

# Function application/mapping (numpy)
df14 = pd.DataFrame(np.random.randn(4, 3), columns=list('bde'), index=['Utah', 'Ohio', 'Texas', 'Oregon'])
print(f"Abs\n{np.abs(df14)}")
print(f"Apply\n{df14.apply(lambda x: x.sum())}") # per column
print(f"Apply2\n{df14.apply(lambda x: x.sum(), axis='columns')}") # per row

def f(x):
    return pd.Series([x.min(), x.max()], index=['min', 'max'])

print(f"Apply3\n{df14.apply(f)}") # per column, return series

df15 = pd.DataFrame(np.arange(12).reshape((4, 3)), columns=list('bde'), index=['Utah', 'Ohio', 'Texas', 'Oregon'])
format = lambda x: 'INV{0:0>7d}'.format(x)
print(f"Apply4\n{df15.applymap(format)}") # per element, reformat

# Sorting, optional 'ascending=False'
df16 = pd.DataFrame(np.arange(8).reshape((2, 4)), index=['three', 'one'], columns=['d', 'a', 'b', 'c'])
print(f"Sort\n{df16.sort_index()}") # by row
print(f"Sort2\n{df16.sort_index(axis=1)}") # by col
print(f"Sort3\n{df16.sort_values(by=['a', 'b'])}") # sort by multiple column values

# Ranking, can use method='dense' for a DENSE_RANK like functionality
df17 = pd.DataFrame({'b': [4.3, 7, -3, 2], 'a': [0, 1, 0, 1], 'c': [-2, 5, 8, -2.5]})
print(f"Rank1\n{df17.rank(axis='columns')}") # ranks rows

# Duplicate index labels
df18 = pd.DataFrame(np.random.randn(4, 3), index=['a', 'a', 'b', 'b'])
print(f"Labels\n{df18.loc['b']}") # returns all elements matching index

# Aggregate functions, handles NaN gracefully.
df19 = pd.DataFrame([[1.4, np.nan], [7.1, -4.5], [np.nan, np.nan], [0.75, -1.3]], index=['a', 'b', 'c', 'd'], columns=['one', 'two'])
print(f"Sum\n{df19.sum()}") # sums cols
print(f"Sum2\n{df19.sum(axis='columns')}") # sums rows, takes NaN as zero
print(f"Sum3\n{df19.sum(axis='columns', skipna=False)}") # sums rows
print(f"Index Max\n{df19.idxmax()}") # index with max
print(f"Cumulative Sum\n{df19.cumsum()}")
print(f"Cumulative Stats\n{df19.describe()}")
