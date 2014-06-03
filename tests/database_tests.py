from squeezerp.database.database_core import DatabaseOperations
from squeezerp.database import database_queries

db = DatabaseOperations()
db.create_all_tables(database_queries.create_tables())
db.close()