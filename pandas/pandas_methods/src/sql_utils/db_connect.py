import urllib
import sqlalchemy as sql

def get_connection(cnxn_str):
    """
    """

    # Pandas/SqlAlchemy
    params = urllib.parse.quote_plus(cnxn_str) # must url-escape delimiters
    hero_engine = sql.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    return hero_engine
