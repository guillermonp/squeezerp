from squeezerp.data_warehouse.database_core import Database
from squeezerp.data_warehouse import database_queries

db = Database()

for table in database_queries.create_tables():
    db.create_table(table)

db.close()