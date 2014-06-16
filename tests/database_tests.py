from squeezerp.database.database_core import DatabaseOperations
from squeezerp.database import database_queries
from squeezerp import resources

db = DatabaseOperations()

#DatabaseOperations().create_all_tables(database_queries.create_tables())
#DatabaseOperations().sql_script(resources.DATABASE_SCHEMA)
#DatabaseOperations().insert_initial_data(database_queries.insert_initial())
#DatabaseOperations().sql("select * from table", " where field1 = '2'", " order by field1 desc")
data = db.execute_query_results(database_queries.select_all.format('DataUploaderHistory'))
print data
a = DatabaseOperations().fetch_query_results(data)
print isinstance(a, DatabaseOperations)