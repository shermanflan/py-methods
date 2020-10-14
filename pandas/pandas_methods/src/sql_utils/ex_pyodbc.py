import pyodbc

def ex_db(cnxn_str):

    # This calls cnxn.commit() when going out of scope.
    with pyodbc.connect(cnxn_str, autocommit=False) as cnxn, \
        pyodbc.connect(cnxn_str, autocommit=False) as cnxn2, \
        pyodbc.connect(cnxn_str, autocommit=True) as cnxn3:

        cursor = cnxn.cursor()
        cursor2 = cnxn2.cursor()
        cursor3 = cnxn3.cursor()

        qry1 = """
            SELECT  ID
                    , API
                    , WKID
            FROM    dbo.DirectionalSurvey WITH (READUNCOMMITTED)
            WHERE   ID > ?;
        """
        
        # Iterate through result set, row by row
        for row in cursor.execute(qry1, 0):
            print(f"{row.ID}, {row.API}, {row.WKID}") 
        
        cmd1 = """
            INSERT INTO dbo.Well VALUES(?, ?, ?)
        """

        # Insert and auto-commit (not atomic)
        count = cursor3.execute(cmd1, "API4", 3.30, 3.30).rowcount
        print(f"Inserted {count} rows")

        # Insert atomically with batch feature
        try:
            cnxn3.autocommit = False
            params = [ ('API5', 5.50, 5.50)
                    , ('API6', 6.60, 6.60) 
                    , ('API7', 7.70, 7.70)]
            
            cursor3.fast_executemany = True
            cursor3.executemany(cmd1, params)

        except pyodbc.DatabaseError as err:
            print(err)
            cnxn3.rollback()
        else:
            cnxn3.commit()
        finally:
            cnxn3.autocommit = True

        qry2 = """
            SELECT  ID
                    , API
                    , LATITUDE
                    , LONGITUDE
            FROM    dbo.Well WITH (READUNCOMMITTED)
            WHERE   ID > ?;
        """

        cursor2.execute(qry2, 0)

        # Read full result set into memory
        for row in cursor2.fetchall(): 
            print(f"{row.ID}, {row.API}, {row.LATITUDE}, {row.LONGITUDE}") 
