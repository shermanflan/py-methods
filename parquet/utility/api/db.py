import urllib

from sqlalchemy import create_engine


class SQLHook:

    def __init__(self, host, db, user, password,
                 driver='{ODBC Driver 17 for SQL Server}'):
        self.host = host
        self.db = db
        self.user = user
        self.password = password
        self.driver = driver
        self.sql_engine = None

    def get_engine(self):

        if self.sql_engine:
            return self.sql_engine

        con_str = f'DRIVER={self.driver};SERVER={self.host};DATABASE={self.db};UID={self.user};PWD={self.password}'
        params = urllib.parse.quote_plus(con_str)

        self.sql_engine = create_engine(
            f"mssql+pyodbc:///?odbc_connect={params}",
            echo=False)  # echo's emitted sql

        return self.sql_engine