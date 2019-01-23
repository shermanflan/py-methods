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

# Example of a script with logging, arguments, and db access.
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--srcdir', help='Specifies the source directory containing import files')
    parser.add_argument('--arcdir', help='Specifies the archive directory for imported files')
    parser.add_argument('--file', help='Specifies the json file to import')
    args = parser.parse_args()
    logging.config.dictConfig(getLogConfig())

    if args.file:
        parseiJSONDb(filename=args.file)
    elif args.srcdir and args.arcdir:
        pickFiles(src=args.srcdir, arc=args.arcdir)

def pickFiles(src, arc):
    """
    Processes all files in the source and then archives.
    """
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
                logging.debug(f'Moving to path: {os.path.join(arc, PurePath(fi).name)}')
                shutil.move(src=fi, dst=os.path.join(arc, PurePath(fi).name)) # preserves file metadata

    except Exception as e: # catch all
        logging.error(f'pickFiles: {e}')
        raise

    logging.shutdown()

def parseiJSONDb(filename=r"C:\Users\ricardogu\Desktop\test4.json"):

    """ Using ijson library enables json iteration/streaming (constant memory footprint).
        This implementation loads to the database as it iterates ensuring a constant memory
        footprint.
    """

    # Pass as parameters to defend against SQL injection. Also, supports plan reuse.
    cnxnstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ScratchDB;Trusted_Connection=yes;'
    qryUlti = '''
        INSERT INTO dbo.PerceptUltiCo (ARNumber, CustomerServer, CustomerDatabase, Source, Created, CreatedBy)
        VALUES(?, ?, ?, ?, ?, SYSTEM_USER)
    '''
    qryLegacy = '''
        INSERT INTO dbo.PerceptLegacyCo (ARNumber, CustomerName, CustomerServer, CustomerDatabase, Location, EECount, Source, Created, CreatedBy)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, SYSTEM_USER)
    '''

    server_name = server_db = None
    ultipro = standalone = 0
    tmpCo = tmpAR = tmpEmpInfo = None
    created = datetime.now()
    source = PurePath(filename).name

    try:
        cnxn = pyodbc.connect(cnxnstr, autocommit=False) # creates explicit txn
        cursor = cnxn.cursor()

        # First, scan server metadata.
        with open(filename, "r", encoding="utf-8") as f:
            
            # Use this to get prefix for the json elements.
            parsed = ijson.parse(f) # returns iterator

            for pre, evt, val in parsed: # returns all (prefix, event, value)
                if (pre, evt) == ('server_db', 'string'):
                    server_db = val

                elif (pre, evt) == ('server_name', 'string'):
                    server_name = val

                if server_db and server_name:
                    break

        # Now, scan company metadata.
        with open(filename, "r", encoding="utf-8") as f:
            
            parsed = ijson.parse(f)

            for pre, evt, val in parsed:
                if (pre, evt) == ('ultipro.item.ar_number', 'string'):
                    ultipro += 1
                    cursor.execute(qryUlti, val, server_name, server_db, source, created)
                # New standalone co
                elif (pre, evt) == ('standalone.item', 'start_map'):
                    tmpCo = tmpAR = tmpEmpInfo = None
                    tmpEmpInfo = defaultdict(int)
                elif (pre, evt) == ('standalone.item.employee_info.item.location', 'string'):
                    tmpEmpInfo[val] += 1
                elif (pre, evt) == ('standalone.item.employee_info.item.location', 'null'):
                    # Default null to 'Unknown'
                    tmpEmpInfo['Unknown'] += 1
                elif (pre, evt) == ('standalone.item.company_name', 'string'):
                    tmpCo = val
                elif (pre, evt) == ('standalone.item.ar_number', 'string'):
                    tmpAR = val
                # End standalone co
                elif (pre, evt) == ('standalone.item', 'end_map'):
                    if tmpEmpInfo: # ignore N/A
                        standalone += 1
                        for loc in tmpEmpInfo.keys():
                            cursor.execute(qryLegacy, tmpAR, tmpCo, server_name, server_db, loc, tmpEmpInfo[loc], source, created)

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

# Execute only if run as the entry point into the program
if __name__ == '__main__':
    main()

