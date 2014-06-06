from squeezerp.database.database_core import DatabaseOperations
from squeezerp.database import database_queries
from squeezerp import resources

DatabaseOperations().sql_script(resources.DATABASE_SCHEMA)
DatabaseOperations().insert_initial_data(database_queries.insert_initial())
DatabaseOperations().sql("select * from table", " where field1 = '2'", " order by field1 desc")