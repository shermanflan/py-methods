import numpy as np
import pandas as pd
import pyodbc as odbc

pepm = pd.read_csv(r'C:\Users\ricardogu\Desktop\Scratch_Data\PEPM\Invoicing_OTF_KCTEST2.csv')

print(f"{pepm.index}")
print(f"{pepm.columns}")

print(f"{pepm[['AR Code', 'PO#', 'tax_code', 'minimumGL']]}") # columns
print(f"{pepm[:5]}") # rows
print(f"Rows&Cols\n{pepm.iloc[:5, :]}")
print(f"Rows&Cols2\n{pepm.iloc[[0, 1, 2], [2, 3, 24]]}") # multi-row, multi-col

print(f"Filter\n{pepm[pepm['AR Code'] == '0']}")
print(f"Filter2\n{pepm.iloc[:, [2, 3, 24, 30, 31, 39]][pepm['AR Code'] == '0']}") # multi-row, multi-col plus predicate
print(f"Filter3\n{pepm.iloc[:, [2, 3, 24, 30, 31, 39]][pepm['Total Invoice'] != 0]}") # multi-row, multi-col plus predicate

col_lengths = pepm[['AR Code', 'PO#']].applymap(lambda x: len(x))
print(f"Apply\n{col_lengths[col_lengths['AR Code'] != 7]}")
print(f"Apply2\n{col_lengths[col_lengths['PO#'] > 255]}")

