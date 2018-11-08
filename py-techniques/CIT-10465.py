import ijson
import pyodbc
from datetime import datetime
from collections import defaultdict

# TODO: Is the shared folder on the same data center host? If not, is it faster
# to copy the file locally first? Test this.
# Looks like O(n):
# Parsed 5000 ultipro, 5 standalone customers (0:00:00.685321)
# Parsed 5000 ultipro, 50 standalone customers (0:00:08.264015)
# Parsed 5000 ultipro, 200 standalone customers (0:00:29.619718)
# Parsed 5000 ultipro, 500 standalone customers (0:01:08.527680)
# Parsed 5000 ultipro, 1000 standalone customers (0:02:25.470764)
# Parsed 5000 ultipro, 2000 standalone customers (0:04:44.362290)
# Loaded 5000 ultipro customers, 599 standalone location counts (0:00:00.762591)
# Loaded 5000 ultipro customers, 5982 standalone location counts (0:00:01.395945)
# Loaded 5000 ultipro customers, 23956 standalone location counts (0:00:03.749685)
# Loaded 5000 ultipro customers, 59864 standalone location counts (0:00:08.115112)
# Loaded 5000 ultipro customers, 119684 standalone location counts (0:00:16.097422)
# Loaded 5000 ultipro customers, 239269 standalone location counts (0:00:35.737822)
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
            #print('\n'.join(list(parsed)))

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
    parseiJSON()

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()

