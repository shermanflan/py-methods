import pyodbc
import datetime

cnxnstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ScratchDB;Trusted_Connection=yes;'
qry = '''
    INSERT INTO dbo.BreachImpact(AR__c, company_name, server_name, server_db, Created)
    VALUES(?, ?, ?, ?, ?)
'''

try:

    cnxn = pyodbc.connect(cnxnstr)
    cursor = cnxn.cursor()

except Exception as e:
    print(e)

try:
    AR__c, company_name = ('server1', 'db1')
    server_name, server_db = ('server1', 'db1')

    # "Sun 10 May 2015 13:54:36 -0700"
    Created = datetime.datetime.now() #.strptime('2018-11-07 14:56:41', "%Y-%m-%d %H:%M:%S")
    
    # Pass as parameters to defend against SQL injection.
    cursor.execute(qry, AR__c, company_name, server_name, server_db, Created)
    cnxn.commit()
    cursor.close()
    cnxn.close()
    
    
except Exception as e:
    print(e)