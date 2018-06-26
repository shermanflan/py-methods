import pyodbc 

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:localhost' 
database = 'ScratchDB' 
username = 'pydemo' 
password = 'pydemo' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

# Insert query - requires commit
qry = '''INSERT [dbo].[Test01] (SVAL, NVAL) 
VALUES (?, ?);
'''

try:
    cursor.execute(qry, ('Weasel21', 0))
    cnxn.commit()
except pyodbc.IntegrityError as e:
    print(e)

# Select query
qry = '''SELECT [SVAL], [NVAL]
  FROM [dbo].[Test01];
'''
cursor.execute(qry) 
row = cursor.fetchone()

while row: 
    print('{0}, {1}'.format(row[0], row[1]))
    row = cursor.fetchone()

# Select query
qry = '''SELECT [SVAL], [NVAL]
  FROM [dbo].[Test01];
'''
cursor.execute(qry) 
rows = cursor.fetchall()

print(rows)

cursor.close()
cnxn.close()