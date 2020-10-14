import logging

import psycopg2

logger = logging.getLogger(__name__)
#logger.setLevel(level=logging.DEBUG)


# TODO: Look at this thread to see if performance can be improved.
# https://github.com/geopandas/geopandas/issues/595
class PgWriter(object):

    def __init__(self, **connect_args):
        self.__connect_args = connect_args
        self.datastore = None
        self.__cursor = None

    def __enter__(self):
        self.datastore = psycopg2.connect(**self.__connect_args)
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

        raise NotImplementedError("TODO")

    def write_batch(self, dml, batch, auto_commit=False):

        raise NotImplementedError("TODO")

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
