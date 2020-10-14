import logging

import pyodbc

logger = logging.getLogger(__name__)
#logger.setLevel(level=logging.DEBUG)


class MsWriter:

    def __init__(self, **connect_args):

        self.__connect_string = 'DRIVER={driver};SERVER={host};DATABASE={db};UID={uid};PWD={pwd};'.format(
            **connect_args
        )
        self.datastore = None
        self.__cursor = None

    def __enter__(self):
        self.datastore = pyodbc.connect(self.__connect_string,
                                        autocommit=False)
        self.__cursor = self.datastore.cursor()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.__cursor.close()
            self.__cursor = None
            self.datastore.close()
            self.datastore = None
        else:
            logger.error(exc_val)

        return False  # propagate errors

    def write_record(self, dml, record, auto_commit=False):

        try:
            self.__cursor.execute(dml, record)

            if auto_commit:
                self.datastore.commit()

        except Exception as e:
            self.datastore.rollback()
            raise e

    def set_input_size(self, size):

        input_sizes = [None] * size + \
                      [(pyodbc.SQL_VARBINARY, 0, 0)]
        self.__cursor.setinputsizes(input_sizes)

    def write_batch(self, dml, batch, auto_commit=False):
        try:
            self.__cursor.fast_executemany = True
            self.__cursor.executemany(dml, batch)

            if auto_commit:
                self.datastore.commit()

        except Exception as e:
            self.datastore.rollback()
            raise e

    def execute_script(self, path, auto_commit=False):

        with open(path, 'r') as f:
            try:
                self.__cursor.execute(f.read())

                if auto_commit:
                    self.datastore.commit()

            except Exception as e:
                self.datastore.rollback()
                raise e

    def execute_dml(self, dml, auto_commit=False):

        try:
            self.__cursor.execute(dml)

            if auto_commit:
                self.datastore.commit()

        except Exception as e:
            self.datastore.rollback()
            raise e

    def batch_commit(self):
        self.datastore.commit()
