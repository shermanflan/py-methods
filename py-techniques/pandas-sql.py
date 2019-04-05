import sqlalchemy as sqla
import pandas as pd
import urllib

cnxnstr = r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ScratchDB;Trusted_Connection=yes;"
params = urllib.parse.quote_plus(cnxnstr) # must url-escape delimiters

db = sqla.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

sqlcmd = """
SELECT	[DEPTNO]
		,[DNAME]
		,[LOC]
FROM	[dbo].[DEPT] WITH (READUNCOMMITTED)
"""

df1 = pd.read_sql(sqlcmd, db)

print(f"{df1[df1['LOC'] == 'NEW YORK']}")