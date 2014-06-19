"""Database - CORE"""

import sqlite3
from squeezerp import resources
from squeezerp.database import database_queries


class Database(object):
    def __init__(self):
        self.db_name = resources.DATABASE
        self.db_conn = sqlite3.connect(self.db_name)
        self.db_query = None

    def _execute_query(self, query, param=None):
        _cursor = self.db_conn.cursor()
        if param is None:
            try:
                _cursor.execute(query)
                self.db_conn.commit()
            except sqlite3.Error as e:
                self.db_conn.rollback()
                print "An error occurred:", e.args[0]
        else:
            try:
                _cursor.execute(query, param)
                self.db_conn.commit()
            except sqlite3.Error as e:
                self.db_conn.rollback()
                print "An error occurred:", e.args[0]

    def close(self):
        if self.db_conn:
            self.db_conn.close()


class DatabaseOperations(Database):
    """
    Database operations: relational database operations
        - CREATE (create new tables)
        - INSERT (adding rows to a table)
        - READ (SELECT) (reading data from a database)
        - UPDATE (updating fields in a table)
        - DELETE (deleting rows from a table)
    """
    def __init__(self):
        super(DatabaseOperations, self).__init__()

    def sql(self, query, snippets):
        """
        Run custom queries:
            db = DatabaseOperations()
            db.sql("select * from table")
            db.sql("select * from {0}".format(table))
            ...
        Add sql snippets:
            " where ..."
            " order by ..."
            " group by ..."
            " having ..."

            db.sql("select * from table", [" where field1 = '2'", " order by field1 desc"])
            db.sql("select * from table" , [where_option1, group_option2, order_option1])
        """
        if snippets:
            snippet = ''.join(snippets)
            sql_query = query + snippet
        else:
            sql_query = query

        self._execute_query(sql_query)

    def sql_fetch_data(self, query, snippets):

        if snippets:
            snippet = ''.join(snippets)
            sql_query = query + snippet
        else:
            sql_query = query

        sql_result = self.db_conn.cursor().execute(sql_query)

        try:
            data = sql_result.fetchall()
            headers = [field[0] for field in sql_result.description]
            return headers, data
        except sqlite3.Error as e:
            print "no results from the query:", e.args[0]

    def sql_script(self, script_path):
        """
        Execute a sql_script (e.g. script.sql)
            The main purpose is create schema from .sql files.
            it might substitute create_all_tables()
        """
        script = open(script_path, 'r').read()
        self.db_conn.executescript(script)

    def create_table(self, query):
        """" create a new table """
        self._execute_query(query)

    def create_all_tables(self, tables):
        """
        create a set of tables:
            this methods will be used during the set up and will create all those tables
             to run the application.
        """
        for table in tables:
            self._execute_query(table)

    def insert_initial_data(self, operations):
        """
        insert values to some fixed tables:
            ItemTypes
            DataUploaderHistoryStatus
            DataUploaderHistoryFormats
        """
        for op in operations:
            self._execute_query(op)

    def insert_history_uploader(self, fields):
        query = database_queries.insert_datauploader
        self._execute_query(query, fields)

    def insert_category(self, c_id, c_name, c_description=None):
        """
        Add new category to table "Categories"

        :param c_id: Categories.id
        :param c_name: Categories.name
        :param c_description: Categories.description
        """
        fields = (c_id, c_name, c_description)
        query = database_queries.insert_category
        self._execute_query(query=query, param=fields)

    def insert_family(self, f_id, f_name, c_id, f_description=None):
        """
        Add new family to table "Families"

        :param f_id: Families.id
        :param f_name: Families.name
        :param c_id: Families.category_id
        :param f_description: Families.description
        """
        fields = (f_id, f_name, c_id, f_description)
        query = database_queries.insert_family
        self._execute_query(query=query, param=fields)

    def insert_vat(self, v_name, value, eq):
        """
        Add new Value-added tax to table "VAT"

        :param v_name: VAT.name
        :param value: VAT.value
        :param eq: VAT.equalisation_tax
        """
        fields = (v_name, value, eq)
        query = database_queries.insert_vat
        self._execute_query(query=query, param=fields)

    def insert_warehouse(self, w_name, w_description, w_location):
        """
        Add new warehouse to table "Warehouses"

        :param w_name: Warehouses.name
        :param w_description: Warehouses.description
        :param w_location: Warehouses.location
        """
        fields = (w_name, w_description, w_location)
        query = database_queries.insert_warehouse
        self._execute_query(query=query, param=fields)