
-- remove previous tables if exist
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Families;
DROP TABLE IF EXISTS VAT;
DROP TABLE IF EXISTS Warehouses;
DROP TABLE IF EXISTS ItemTypes;
DROP TABLE IF EXISTS DataUploaderHistory;
DROP TABLE IF EXISTS DataUploaderHistoryStatus;
DROP TABLE IF EXISTS DataUploaderHistoryFormats;

--Create new schema:

-- table "Categories"

CREATE TABLE Categories(
    id INTEGER PRIMARY KEY ASC NOT NULL,
    name TEXT NOT NULL,
    description TEXT
);

-- table "Families"

CREATE TABLE Families(
    id INTEGER PRIMARY KEY ASC NOT NULL,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    description TEXT,
    FOREIGN KEY(category_id) REFERENCES Categories(id),
    UNIQUE(category_id, id) ON CONFLICT ROLLBACK
);

-- table "VAT" Value added tax

CREATE TABLE VAT(
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    value REAL NOT NULL,
    equalisation_tax REAL NOT NULL,
    UNIQUE(name, value, equalisation_tax) ON CONFLICT ROLLBACK
);

-- table "Warehouses"

CREATE TABLE Warehouses(
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    location TEXT,
    UNIQUE(name, description, location) ON CONFLICT ROLLBACK
);

-- table "DataUploaderHistory": uploading task results

CREATE TABLE DataUploaderHistory(
    id INTEGER PRIMARY KEY ASC NOT NULL,
    sheet_name TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    file_format INTEGER NOT NULL,
    has_error INTEGER NOT NULL,
    records_found INTEGER NOT NULL,
    errors INTEGER NOT NULL,
    status INTEGER NOT NULL,
    init TEXT NOT NULL,
    finish TEXT NOT NULL
);

-- table "DataUploaderHistoryStatus": success and errors

CREATE TABLE DataUploaderHistoryStatus(
    id INTEGER PRIMARY KEY NOT NULL,
    status_msg TEXT NOT NULL
);

-- table "DataUploaderHistoryFormats" : xls and csv files

CREATE TABLE DataUploaderHistoryFormats(
    id INTEGER PRIMARY KEY NOT NULL,
    input_format TEXT NOT NULL
);

-- table "ItemTypes": Items, Services and Labors
CREATE TABLE ItemTypes(
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL
);