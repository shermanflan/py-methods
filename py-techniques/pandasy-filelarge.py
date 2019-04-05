import numpy as np
import pandas as pd
import pyodbc as odbc
import csv

# Utility functions
def clean(s):
    return s.strip()

# The only attributes required from OCC are Well Name, API Number, Well Status, Spud Date and First Production Date
file = r'C:\Users\rguzman\Desktop\W27base\W27base.csv'
csv_file = r'C:\Users\rguzman\Desktop\W27base\extract.csv'
csv_file2 = r'C:\Users\rguzman\Desktop\W27base\extract2.csv'

# Example 1: Read first 10 rows.
#okc_wells = pd.read_csv(file, nrows=10)
#print(f"{list(okc_wells.columns)}")
#print(f"{okc_wells[['API_Number', 'Well_Name', 'Well_Status', 'Spud', 'First_Prod']]}")

# Example 2: Read in chunks (via an iterator)
chunksize=10
okc_wells_iter = pd.read_csv(file, chunksize=chunksize)

with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['API_Number', 'Well_Name', 'Well_Status', 'Spud', 'First_Prod'])
    
    i, stopat = 0, 10
    for chunk in okc_wells_iter:
        # Clean data
        chunk['Well_Name'] = chunk['Well_Name'].apply(clean)
        tmp_df = chunk[['API_Number', 'Well_Name', 'Well_Status', 'Spud', 'First_Prod']]

        # Built in export
        # tmp_df.to_csv(csv_file2, index=False)

        for row in tmp_df.index:
            writer.writerow(tmp_df.loc[row])

        i += 1
        if i > stopat:
            break


