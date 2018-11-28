import argparse
import ijson
import pyodbc
from datetime import datetime
from collections import defaultdict
import os
import shutil
from pathlib import Path, PurePath
import re
import logging.config

# Entry point
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--srcdir', help='Specifies the source directory containing import files')
    parser.add_argument('--arcdir', help='Specifies the archive directory for imported files')
    parser.add_argument('--file', help='Specifies the json file to import')
    parser.add_argument('--db', help='Specifies the database connection string')
    args = parser.parse_args()

    if args.file:
        #if args.db:
        parseiJSONDb(filename=args.file)
    elif args.srcdir and args.arcdir:
        pickFiles(src=args.srcdir, arc=args.arcdir)

# TODO: Is the shared folder on the same data center host? If not, is it faster
# to copy the file locally first? Test this.
def pickFiles(src, arc):
    """
    Processes all files in the source and then archives.
    """
    logging.config.dictConfig(getLogConfig())
    newfiles = []
    
    try:
        rex = r"""
                ^
                .*                  # server name
                _breach_report_
                \d\d-\d\d           # MM-DD
                .json
                $
            """
        p = re.compile(rex, re.IGNORECASE | re.VERBOSE)

        with os.scandir(path=src) as d:
            for entry in d: # os.DirEntry
                # Use pattern match to identify breach import files.
                if entry.is_file() and p.match(entry.name):
                    newfiles.append(entry.path)
            
            if not newfiles:
                logging.error('No files available to import!')
                raise Exception('No files available to import!')

            # Process files atomically (all or nothing).
            for fi in newfiles:
                parseiJSONDb(filename=fi)

            # Ok, all good -> archive.
            for fi in newfiles:
                shutil.move(src=fi, dst=os.path.join(arc, entry.name)) # preserves file metadata

    except Exception as e: # catch all
        logging.error(f'pickFiles: {e}')
        raise

    logging.shutdown()

def parseiJSONDb(filename=r"C:\Users\ricardogu\Desktop\test4.json"):

    """ Using ijson library enables json iteration/streaming (constant memory footprint).
        This implmentation loads to the database as it iterates ensuring a constant memory
        footprint.
    """

    # Pass as parameters to defend against SQL injection. Also, supports plan reuse.
    cnxnstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ScratchDB;Trusted_Connection=yes;'
    qryUlti = '''
        INSERT INTO dbo.BreachImpact(AR__c, Source, Created, CreatedBy)
        VALUES(?, ?, ?, SYSTEM_USER)
    '''
    qryLegacy = '''
        INSERT INTO dbo.BreachImpact(AR__c, company_name, location, EECount, Source, Created, CreatedBy)
        VALUES(?, ?, ?, ?, ?, ?, SYSTEM_USER)
    '''
    qryMeta = '''
        UPDATE dbo.BreachImpact
            SET server_name = ?
                , server_db = ?
        WHERE   Source = ?
    '''
    server_name = server_db = None
    ultipro = standalone = 0
    tmpCo = tmpAR = tmpEmpInfo = None
    created = datetime.now()
    p = PurePath(filename).name

    try:
        cnxn = pyodbc.connect(cnxnstr)
        cursor = cnxn.cursor()

        with open(filename, "r", encoding="utf-8") as f:
            
            # Use this to get prefix for the json elements.
            parsed = ijson.parse(f) # returns iterator

            for pre, evt, val in parsed: # returns all (prefix, event, value)
                if (pre, evt) == ('server_db', 'string'):
                    server_db = val
                elif (pre, evt) == ('server_name', 'string'):
                    server_name = val
                elif (pre, evt) == ('ultipro.item.ar_number', 'string'):
                    ultipro += 1
                    cursor.execute(qryUlti, val, p, created)
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
                        standalone += 1
                        for loc in tmpEmpInfo.keys():
                            cursor.execute(qryLegacy, tmpAR, tmpCo, loc, tmpEmpInfo[loc], p, created)

            cursor.execute(qryMeta, server_name, server_db, p)

        cnxn.commit()
        cursor.close()
        cnxn.close() # rolls back any uncommitted changes

        elapsed = datetime.now() - created
        logging.info(f'Parsed {ultipro} ultipro, {standalone} standalone customers ({elapsed})')

    except Exception as e:
        # As long as your connection and cursors are not used outside the current function, 
        # they will be closed automatically and immediatley when the function exits.
        logging.error(f'parseiJSONDb: {e} for {filename}')
        raise

def getLogConfig():
    return {
                'version': 1,
                'disable_existing_loggers': False,
                'formatters': { 
                    'standard': { 
                        'format': '%(asctime)s [%(levelname)s]: %(message)s'
                    }
                },
                'handlers': { 
                    'default': { 
                        'level': 'INFO',
                        'formatter': 'standard',
                        'class': 'logging.handlers.RotatingFileHandler',
                        'filename': 'CIT-10465.log',
                        'maxBytes': 1024*1024,
                        'backupCount': 3
                    }
                },
                'loggers': { 
                    '': { 
                        'handlers': ['default'],
                        'level': 'INFO',
                        'propagate': True
                    }
                }
            }

def parseiJSON(filename=r"C:\Users\ricardogu\Desktop\test4.json"):

    """ Using ijson library enables json iteration/streaming (constant memory footprint).
        However, keeping the object tree in memory does create additional memory overhead.
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
        logging.info(f'Parsed {len(ultipro)} ultipro, {len(standalone)} standalone customers ({elapsed})')

    except Exception as e:
        logging.error(f'parseiJSON: {e} for {filename}')
        return

    # Import data
    dbLoad(server_db, server_name, ultipro, standalone, filename)

# TODO: If loads are too slow, replace this with a CSV export + BULK import.
def dbLoad(server_db, server_name, ultipro, standalone, filename):

    ''' Load to db
    '''

    cnxnstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ScratchDB;Trusted_Connection=yes;'
    qry = '''
        INSERT INTO dbo.BreachImpact(AR__c, company_name, server_name, server_db, location, EECount, Source, Created, CreatedBy)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, SYSTEM_USER)
    '''
    p = PurePath(filename).name

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
            cursor.execute(qry, ar, None, server_name, server_db, None, 0, p, created)
        
        socounts = 0
        for co in standalone:
            for loc in co[2].keys():
                #print(loc, len(loc))
                cursor.execute(qry, co[1], co[0], server_name, server_db, loc, co[2][loc], p, created)
                socounts += 1
        
        cnxn.commit()
        cursor.close()
        cnxn.close() # rolls back any uncommitted changes
        
        elapsed = datetime.now() - created
        logging.info(f'Loaded {len(ultipro)} ultipro customers, {socounts} standalone location counts ({elapsed})')

    except Exception as e:
        # As long as your connection and cursors are not used outside the current function, 
        # they will be closed automatically and immediatley when the function exits.
        logging.error(f'Error: {e}')
        raise

# Execute only if run as the entry point into the program
if __name__ == '__main__':
    main()

