"""SQL queries to create, read, update and delete (CRUD)"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CREATE TABLES
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def create_tables():
    return [create_categories, create_families, create_VAT, create_itemTypes, create_warehouses,
            create_datatools_history]


create_categories = """
                    CREATE TABLE Categories(
                    id INTEGER PRIMARY KEY ASC NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT)
                    """

create_families = """
                    CREATE TABLE Families(
                    id INTEGER PRIMARY KEY ASC NOT NULL,
                    name TEXT NOT NULL,
                    category_id INTEGER NOT NULL,
                    description TEXT,
                    FOREIGN KEY(category_id) REFERENCES Categories(id),
                    UNIQUE(category_id, id) ON CONFLICT ROLLBACK)
                    """

create_VAT = """
                CREATE TABLE VAT(
                id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                value REAL NOT NULL,
                equalisation_tax REAL NOT NULL,
                UNIQUE(name, value, equalisation_tax) ON CONFLICT ROLLBACK)
                """

create_itemTypes = """
                    CREATE TABLE ItemTypes(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL)
                    """

create_warehouses = """
                    CREATE TABLE Warehouses(
                    id INTEGER PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    location TEXT,
                    UNIQUE(name, description, location) ON CONFLICT ROLLBACK)
                    """

create_datatools_history = """
                            CREATE TABLE DataUploaderHistory(
                            id INTEGER PRIMARY KEY NOT NULL,
                            sheet_name TEXT NOT NULL,
                            file_name TEXT NOT NULL,
                            file_size INTEGER NOT NULL,
                            file_format TEXT NOT NULL,
                            has_error INTEGER NOT NULL,
                            records_found REAL NOT NULL,
                            errors INTEGER NOT NULL,
                            error_msg TEXT NOT NULL,
                            start TEXT NOT NULL,
                            end TEXT NOT NULL)
                            """


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# INSERT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
insert_category = 'INSERT INTO Categories (id, name, description) VALUES (?, ?, ?)'

insert_family = 'INSERT INTO Families (id, name, category_id, description) VALUES (?, ?, ?, ?);'

insert_vat = 'INSERT INTO VAT(name, value, equalisation_tax) VALUES (?, ?, ?);'

insert_items_type = """
                    INSERT INTO ItemTypes
                        SELECT 1 AS 'id', 'Items' AS 'name'
                    UNION SELECT 2, 'Services'
                    UNION SELECT 3, 'Labor';
                    """

insert_warehouse = 'INSERT INTO Warehouses (name, description, location) VALUES (?, ?, ?);'

insert_datauploader = """
                        INSERT INTO DataUploaderHistory
                        (sheet_name, file_name, file_size, file_format, has_error, records_found, errors, error_msg,
                        start, end) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """