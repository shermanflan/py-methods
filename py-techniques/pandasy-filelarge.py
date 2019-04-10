import numpy as np
import pandas as pd
import pyodbc as odbc
import csv
import re
import sqlalchemy as sqla
import urllib
from datetime import datetime

# DB setup
cnxnstr = r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ScratchDB;Trusted_Connection=yes;"
params = urllib.parse.quote_plus(cnxnstr) # must url-escape delimiters

db = sqla.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# Utility functions
def clean(s):
    return s.strip()

# The only attributes required from OCC are Well Name, API Number, Well Status, Spud Date and First Production Date
file = r'C:\Users\rguzman\Desktop\W27base\W27base.csv'
csv_file = r'C:\Users\rguzman\Desktop\W27base\extract.csv'
csv_file2 = r'C:\Users\rguzman\Desktop\W27base\extract2.csv'

# Example 1: Read first 10 rows.
okc_wells = pd.read_csv(file, nrows=10, parse_dates=True)
print(f"{list(okc_wells.columns)}")
#print(f"{okc_wells[['API_Number', 'Well_Name', 'Well_Status', 'Spud', 'First_Prod']]}")

# Example 2: Read in chunks (via an iterator)
chunksize=1000
cols = ['API_Number', 'Well_Name', 'Operator_Name', 'Well_Status', 'Spud', 'First_Prod', 'Total_Depth', 'Well_Type', 'OilBBL_PerDay', 'Oil_Volume', 'WellTypeKey', 'Spud_Year']
outcols = ['API_Number', 'Well_Name', 'Operator_Name', 'Well_Status', 'Spud', 'First_Prod', 'Total_Depth', 'Well_Type', 'OilBBL_PerDay', 'Oil_Volume', 'WellTypeID', 'Spud_Year']
okc_wells_iter = pd.read_csv(file, chunksize=chunksize)

volume_bins = [0.0, 100.0, 5000.0, 10000.0]
volume_names = ['Low (<100)', 'Medium (<5K)', 'High (<10K)']

pattern = r'Llc'
regex = re.compile(pattern, flags=re.IGNORECASE)

sqlcmd = """
SELECT	WellTypeID, WellTypeName
FROM	dbo.DimWellType;
"""
welltypes = pd.read_sql(sqlcmd, db)

with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(cols)
    
    i, stopat = 0, 10
    for chunk in okc_wells_iter:
        chunk['Oil_Volume'] = None # add new column
        chunk['WellTypeKey'] = None
        chunk['Spud_Year'] = None

        # Clean & transform data
        chunk['Well_Name'] = chunk['Well_Name'].apply(clean)
        tmp_df = chunk[cols].dropna(how='all') # drops all rows containing no data
        tmp_df['Well_Name'] = tmp_df['Well_Name'].map(lambda x: x.strip().title())
        tmp_df['Operator_Name'] = tmp_df['Operator_Name'].map(lambda x: regex.sub('LLC', x.strip().title())) # simple regex example
        tmp_df['Well_Type'] = tmp_df['Well_Type'].map(lambda x: x.strip().upper())

        tmp_df = tmp_df.drop_duplicates(keep='last') # can also specify a set of columns via a list
        tmp_df.fillna({'Well_Status': 'UNKNOWN', 'Well_Type': 'UNKNOWN'}, inplace=True) # fill in missing values with a default
        tmp_df['Well_Type'].replace('', 'UNKNOWN', inplace=True) # replace blank value
        tmp_df['Spud'].replace('1900-01-01', '', inplace=True) # replace sentinel date
        tmp_df['First_Prod'].replace('1900-01-01', '', inplace=True) # replace sentinel date

        # Join/lookup
        tmp_df = pd.merge(tmp_df, welltypes, left_on='Well_Type', right_on='WellTypeName', how='inner') # also left, right, outer

        # Group By
        grp1 = tmp_df['Total_Depth'].groupby(tmp_df['Operator_Name'])
        #print(f"Mean: {grp1.mean()}, Count: {grp1.size()}") # also min, max

        # Iterate group
        #for name, group in grp1:
        #    print(f"Name: {name}")
        #    print(f"Group: {group}")

        # Put into dict
        #pieces = dict(list(grp1))
        #if 'Chesapeake Operating LLC' in pieces:
        #    print(f"Chesapeake: {pieces['Chesapeake Operating LLC']}")

        # Group by 2: 1962-01-27
        tmp_df['Spud_Year'] = tmp_df['Spud'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").year if x else 0)
        grp2 = tmp_df['Well_Name'].groupby(tmp_df['Spud_Year'])
        #print(grp2.size())

        # Discretize
        tmp_df['Oil_Volume'] = pd.cut(tmp_df['OilBBL_PerDay'], volume_bins, labels=volume_names, right=False)

        # Built in export
        # tmp_df.to_csv(csv_file2, index=False)

        # CSV export
        for row in tmp_df.index:
            writer.writerow(tmp_df.loc[row, outcols])

        i += 1
        if i > stopat:
            break

print(f'Complete')