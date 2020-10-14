import os
import urllib


_DRIVER = os.environ['DB_DRIVER']
_SERVER = os.environ['DB_SERVER']
_DATABASE = os.environ['DB']
_USERNAME = os.environ['DB_USER']
_PASSWORD = os.environ['DB_PWD']
_CNXN_STR = 'DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4}'.format(
    _DRIVER, _SERVER, _DATABASE, _USERNAME, _PASSWORD
)
_PARAMS = urllib.parse.quote_plus(_CNXN_STR)  # must url-escape delimiters

ENGINE_OPTS = {
    'echo': bool(os.environ['SQLALCHEMY_DEBUG']),
    'isolation_level': 'READ_UNCOMMITTED'
}
SESSION_OPTS = {
    'autocommit': True
}

_TRACK_NOTIFY = bool(os.environ['SQLALCHEMY_TRACK_MODIFICATIONS'])
_DB_URI = f"mssql+pyodbc:///?odbc_connect={_PARAMS}"

APP_CONFIG = {
    'SQLALCHEMY_DATABASE_URI': _DB_URI,
    'SQLALCHEMY_TRACK_MODIFICATIONS': _TRACK_NOTIFY,
    'APP_SECRET': os.environ['APP_SECRET']
}