from pandas_methods.src.sql_utils.db_connect import get_connection
import pandas_methods.src.sql_utils.ex_pyodbc as odbc
import pandas_methods.src.pandas_utils.db_pandas as px

def main():

    driver = '{ODBC Driver 17 for SQL Server}'
    server = 'sql-fabulous' 
    database = 'ScratchDB' 
    username = 'sa' 
    password = 'HelloWorld1'
    cnxn_str = 'DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4}'.format(
        driver, server, database, username, password
    )

    # SQL Alchemy engine
    hero_engine = get_connection(cnxn_str)

    print(f"pandas examples...")
    px.df_operations(hero_engine)

    print(f"pyodbc examples...")
    odbc.ex_db(cnxn_str)

if __name__ == "__main__":

    main()