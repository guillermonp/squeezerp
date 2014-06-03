"""
Database - CORE:
    - create tables

"""
import sqlite3
from squeezerp import resources
from . import database_queries


class Database:
    def __init__(self):
        self.db_name = resources.DATABASE
        self._connection = sqlite3.connect(self.db_name)

    def _execute_query(self, query, param=None):
        _cursor = self._connection.cursor()
        if param is None:
            try:
                _cursor.execute(query)
                self._connection.commit()
            except sqlite3.Error as e:
                self._connection.rollback()
                print "An error occurred:", e.args[0]
        else:
            try:
                _cursor.execute(query, parameters=param)
                self._connection.commit()
            except sqlite3.Error as e:
                self._connection.rollback()
                print "An error occurred:", e.args[0]

    def close(self):
        if self._connection:
            self._connection.close()


class DatabaseOperations(Database):
    """
    Database operations:
        - CREATE (create new tables)
        - INSERT (adding rows to a table)
        - READ (SELECT) (reading data from a database)
        - UPDATE (updating fields in a table)
        - DELETE (deleting rows from a table)
    """
    def __init__(self):
        Database.__init__(self)

    def create_table(self, query):
        return self._execute_query(query)

    def create_all_tables(self, tables):
        for table in tables:
            self._execute_query(table)

    def insert_history_uploader(self, ws, f_name, f_size, i_type, has_e, records, errors, msg, start, end):
        query = database_queries.insert_datauploader
        param = (ws, f_name, f_size, i_type, has_e, records, errors, msg, start, end)
        self._execute_query(query, param)