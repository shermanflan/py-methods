import argparse
import ijson
import pyodbc
from datetime import datetime
from collections import defaultdict

# TODO: Is the shared folder on the same data center host? If not, is it faster
# to copy the file locally first? Test this.
def parseiJSON(filename=r"C:\Users\ricardogu\Desktop\test4.json"):

    """ Using ijson library enables json iteration/streaming (constant memory footprint).
    """
    server_name = server_db = None
    ultipro, standalone = [], []
    tmpCo = tmpAR = tmpEmpInfo = None
    created = datetime.now()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            
            # Use this to get prefix for the json elements.
            parsed = ijson.parse(f) # returns iterator

            for pre, evt, val in parsed: # returns all (prefix, event, value)
                if (pre, evt) == ('server_db', 'string'):
                    server_db = val
                elif (pre, evt) == ('server_name', 'string'):
                    server_name = val
                elif (pre, evt) == ('ultipro.item.ar_number', 'string'):
                    ultipro.append(val)
                # New standalone co
                elif (pre, evt) == ('standalone.item', 'start_map'):
                    tmpEmpInfo = defaultdict(int)
                elif (pre, evt) == ('standalone.item.employee_info.item.location', 'string'):
                    tmpEmpInfo[val] += 1
                elif (pre, evt) == ('standalone.item.company_name', 'string'):
                    tmpCo = val
                elif (pre, evt) == ('standalone.item.ar_number', 'string'):
                    tmpAR = val
                # End standalone co
                elif (pre, evt) == ('standalone.item', 'end_map'):
                    if tmpEmpInfo: # ignore N/A
                        standalone.append([tmpCo, tmpAR, tmpEmpInfo])

        elapsed = datetime.now() - created
        print(f'Parsed {len(ultipro)} ultipro, {len(standalone)} standalone customers ({elapsed})')

    except Exception as e:
        print(f'Error: {e}')
        return

    # Import data
    dbLoad(server_db, server_name, ultipro, standalone)

# TODO: If loads are too slow, replace this with a CSV export + BULK import.
def dbLoad(server_db, server_name, ultipro, standalone):

    ''' Load to db
    '''

    cnxnstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ScratchDB;Trusted_Connection=yes;'
    qry = '''
        INSERT INTO dbo.BreachImpact(AR__c, company_name, server_name, server_db, location, EECount, Created, CreatedBy)
        VALUES(?, ?, ?, ?, ?, ?, ?, SYSTEM_USER)
    '''

    try:
        # TODO: Which is faster?
        cnxn = pyodbc.connect(cnxnstr, autocommit=False) # creates explicit txn
        #cnxn = pyodbc.connect(cnxnstr)
        cursor = cnxn.cursor()

    except Exception as e:
        print(f'Error: {e}')
        return

    try:
        created = datetime.now() #.strptime('2018-11-07 14:56:41', "%Y-%m-%d %H:%M:%S")
    
        # Pass as parameters to defend against SQL injection. Also, supports plan reuse.
        for ar in ultipro:
            cursor.execute(qry, ar, None, server_name, server_db, None, 0, created)
        
        socounts = 0
        for co in standalone:
            for loc in co[2].keys():
                #print(loc, len(loc))
                cursor.execute(qry, co[1], co[0], server_name, server_db, loc, co[2][loc], created)
                socounts += 1
        
        cnxn.commit()
        cursor.close()
        cnxn.close() # rolls back any uncommitted changes
        
        elapsed = datetime.now() - created
        print(f'Loaded {len(ultipro)} ultipro customers, {socounts} standalone location counts ({elapsed})')

    except Exception as e:
        # As long as your connection and cursors are not used outside the current function, 
        # they will be closed automatically and immediatley when the function exits.

        print(f'Error: {e}')
        return

#
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='Specifies the json file to import')
    parser.add_argument('--db', help='Specifies the database connection string')
    args = parser.parse_args()

    if args.file:
        #if args.db:
        parseiJSON(filename=args.file)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()

