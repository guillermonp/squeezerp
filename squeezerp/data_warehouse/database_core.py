"""
Database - CORE:
    - create tables

"""
import sqlite3
from squeezerp import resources


class Database:
    def __init__(self):
        self.db_name = resources.DATABASE
        self._connection = sqlite3.connect(self.db_name)

    def _execute_query(self, query=None):
        _cursor = self._connection.cursor()
        if query:
            try:
                _cursor.execute(query)
                self._connection.commit()
            except sqlite3.Error as e:
                self._connection.rollback()
                print "An error occurred:", e.args[0]

    def close(self):
        if self._connection:
            self._connection.close()

    def create_table(self, query=None):
        return self._execute_query(query)