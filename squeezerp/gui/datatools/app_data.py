"""
DataTools: Set of variables
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GENERAL:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# sheets - number of columns
SHEETS = {
    "Categories": 3,
    "Families": 4,
    "Items": 29,
    "VAT": 3,
    "PaymentMethods": 1,
    "Warehouses": 3}

DB_TYPES = {
    1: "Text not null",
    2: "Integer not null",
    3: "Real not null",
    4: "Date not null",
    5: 'Text|null',
    6: "Integer|null",
    7: "Real|null",
    8: "Date|null"}

FIELDS_TYPES = {
    "Categories": {0: 2, 1: 1, 2: 5},
    "Families": {0: 2, 1: 1, 2: 2, 3: 5},
    "VAT": {0: 1, 1: 3, 2: 3},
    "PaymentMethods": {0: 1},
    "Warehouses": {0: 1, 1: 5, 2: 5}}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GENERAL - MESSAGES:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HEADER_ERROR = ["type", "row", "column", "message", "error value", "required type"]

ERROR_VAL_MSG = "Input data does not match with the chosen data type"
ERROR_VAL_VALUE = "[{0}]"
ERROR_VAL_CORRECT = "[{0}]"

ERROR_COLUMNS_MSG = "The number of columns = {0} and the number for sheet '{1}' must be {2}. \nReview the input file."

ERROR_READ_CSV_MSG = "Error reading csv file"
ERROR_READ_CSV_CORRECT = "The input file (csv) do not have to contain empty rows"

ERROR_INPUT_OPTION = """Select:\n--xls (green)\n--csv (purple)"""
ERROR_RUN_OPTION = """Select:\n--process until error\n--process all"""
ERROR_FILE_OPTION = """Selected input file does not correspond with selected input type"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXCEL:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CELL_TYPES_XLS = {
    0: "Empty",
    1: "Text",
    2: "Number",
    3: "Date",
    4: "Boolean",
    5: "Error",
    6: "Blank"}

# column_index: cell_type --> {0: 2, 1: 1} --> col= 1 - Number , col=2 - Text
FIELDS_TYPES_XLS = {
    "Categories": {0: [2], 1: [1], 2: [0, 1, 6]},
    "Families": {0: [2], 1: [1], 2: [1], 3: [0, 1, 6]},
    "VAT": {0: [1], 1: [2], 2: [2]},
    "PaymentMethods": {0: [1]},
    "Warehouses": {0: [1], 1: [0, 1, 6], 2: [0, 1, 6]}}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TABLES - HEADERS:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TABLE_HEADERS = {
    "Categories": ["id", "name", "description"],
    "Families": ["id", "name", "category_id", "description"],
    "VAT": ["name", "value", "equalisation_tax"],
    "PaymentMethods": ["description"],
    "Warehouses": ["name", "description", "location"]
}