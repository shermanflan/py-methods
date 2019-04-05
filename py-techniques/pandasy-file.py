import numpy as np
import pandas as pd
import pyodbc as odbc

file = r'C:\Users\rguzman\Desktop\Apartments.csv'

apts = pd.read_csv(file)

print(f"{apts.index}")
print(f"{apts.columns}")

print(f"Cols:\n{apts[['Available', 'Apartment', 'Type', 'Location']]}") # columns
print(f"Rows:\n{apts[:5]}") # rows
print(f"Rows&Cols\n{apts.iloc[:5, :]}")
print(f"Rows&Cols2\n{apts.iloc[[0, 1, 2], [2, 3, 5]]}") # multi-row, multi-col

print(f"Filter\n{apts[apts['Available'].isnull()]}")
print(f"Filter2\n{apts.iloc[:, [2, 3, 5]][apts['Type'] == 'Studio']}") # multi-row, multi-col plus predicate
print(f"Filter3\n{apts.iloc[:, [2, 3, 5]][apts['Type'] != 'Studio']}") # multi-row, multi-col plus predicate

col_lengths = apts[['Apartment', 'Comments']].applymap(lambda x: len(x))
print(f"Apply\n{col_lengths[col_lengths['Apartment'] != 7]}")
print(f"Apply2\n{col_lengths[col_lengths['Comments'] > 10]}")

apts2 = pd.read_csv(file, skiprows=[1, 2, 3]) # sep can also be a regular expression \s+
print(f"Rows:\n{apts2[:]}") # rows
