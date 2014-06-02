"""
DataTools:

-- input type:
    -- .xls files
    -- .csv files
"""

import csv
import datetime
from collections import OrderedDict

import xlrd
import numpy as np

from squeezerp.gui.datatools import app_data as dt


class DataUploader:
    """
    DataUploader allows upload blocks of data from other sources such as .csv, .txt and Excel files.

    Notes:
        import_csv: currently does not provide data type testing.
        import_txt: ""
        import_excel: Includes capabilities to check data types.
    """

    def __init__(self, path, sheet_name, stop_option=False):
        self._path = path
        self._headers = None
        self._sheet = sheet_name
        self._stop = stop_option
        self._type = None

        self._data = None
        self._workbook = None
        self._errors = 0
        self._has_errors = 0
        self._stop_trigger = 0
        self._records_w_errors = []

    def import_csv(self, delimiter, hd_option=True):
        """
        import_csv collect all data from csv
            1) first column is header-- by default
            2) without column headers
        """
        self._type = "csv"
        # Due to each column has its own rules we must keep the dictionary in order.
        self._data = OrderedDict()
        try:
            if hd_option is True:
                with open(self._path, 'rb') as csv_file:
                    reader = csv.DictReader(csv_file, delimiter=delimiter)
                    self._headers = reader.fieldnames

                    for h in self._headers:
                        self._data[h] = []

                    for row in reader:
                        for h, v in zip(self._headers, row):
                            self._data[h].append(row[h])
            else:
                with open(self._path, 'rb') as csv_file:
                    reader = csv.reader(csv_file, delimiter=delimiter)

                    # detect the max. number of columns with values
                    max_cols = max(len(rw) for rw in reader)
                    csv_file.seek(0)

                    self._headers = ['field{0}'.format(c) for c in range(max_cols)]

                    for h in self._headers:
                        self._data[h] = []

                    for row in reader:
                        for col in range(len(self._headers)):
                            self._data[self._headers[col]].append(row[col])
        except (KeyError, IndexError):
            print dt.ERROR_READ_CSV
            self._errors = 1

        # convert to list
        data = self._data.values()
        check = self._check_data_types_csv(data=data)

        if self._errors > 0 or check == 1:
            self._has_errors = 1
        else:
            return data

    def _check_data_types_csv(self, data):
        # Returns 1 - pass test otherwise 0
        sheet = self._sheet
        num_cols = len(data)
        _data = np.array(data)

        # check the number of columns
        if dt.SHEETS[sheet] == num_cols:
            column_types = dt.FIELDS_TYPES[sheet]
            for col in range(num_cols):
                _col = _data[col, :]

                if 1 == column_types[col]:
                    # check if we can convert to string: Text not null
                    for pos, cell in enumerate(_col):
                        if bool(cell.strip()) is False:
                            if self._error_format_csv(col, pos, cell, 1) == 1:
                                return 1

                if 2 == column_types[col]:
                    # import_csv, imports data as strings.
                    # check if we can convert to numeric: Integer not null
                    for pos, cell in enumerate(_col):
                        if self._isint(cell) is False:
                            if self._error_format_csv(col, pos, cell, 2) == 1:
                                return 1

                if 3 == column_types[col]:
                    # check if we can convert to numeric: Real not null
                    for pos, cell in enumerate(_col):
                        if self._isfloat(cell) is False:
                            if self._error_format_csv(col, pos, cell, 3) == 1:
                                return 1

                if 4 == column_types[col]:
                    # check different date formats
                    # create documentation about supported formats
                    for pos, cell in enumerate(_col):
                        if self._isdate(cell) is False:
                            if self._error_format_csv(col, pos, cell, 4) == 1:
                                return 1

                if 5 == column_types[col]:
                    # Text | null
                    for pos, cell in enumerate(_col):
                        if bool(cell.strip()) is True and \
                                (self._isdate(cell) or self._isint(cell) or self._isfloat(cell)):
                            if self._error_format_csv(col, pos, cell, 5) == 1:
                                return 1

                if 6 == column_types[col]:
                    # Integer | null
                    for pos, cell in enumerate(_col):
                        if self._isint(cell) is False or bool(cell.strip()) is False:
                            if self._error_format_csv(col, pos, cell, 6) == 1:
                                return 1

                if 7 == column_types[col]:
                    # Real | null
                    for pos, cell in enumerate(_col):
                        if self._isfloat(cell) is False or bool(cell.strip()) is False:
                            if self._error_format_csv(col, pos, cell, 7) == 1:
                                return 1

                if 8 == column_types[col]:
                    # Date | null
                    for pos, cell in enumerate(_col):
                        if self._isdate(cell) is False or bool(cell.strip()) is False:
                            if self._error_format_csv(col, pos, cell, 8) == 1:
                                return 1
        else:
            print dt.ERROR_COLUMNS.format(num_cols, self._sheet, dt.SHEETS[sheet])
            return 1

    def _error_format_csv(self, col, pos, cell, cell_format):
        cell_format = dt.DB_TYPES[cell_format]
        print (dt.ERROR_VALIDATION.format(pos + 1, col + 1, cell, cell_format))
        self._errors += 1
        if self._stop is True:
            return 1

    def import_excel(self):
        """
        import_excel: Upload data from the selected worksheet.
        steps:
            1) check sheet_name
            2) check number of column - avoid errors by importing other columns
            3) loop until stop_trigger = 1 (True)
        """
        self._type = "xls"
        self._workbook = xlrd.open_workbook(self._path)
        sheet_name = self._sheet
        if sheet_name in dt.SHEETS:
            worksheet = self._workbook.sheet_by_name(sheet_name)
            column_type = dt.FIELDS_TYPES_XLS[sheet_name]
            cols = worksheet.ncols
            cols_sheet = dt.SHEETS[sheet_name]
            # exclude column header
            rows = worksheet.nrows - 1
            # empty array [None] to store data. dtype must be an object due to the array doesn't have an unique type
            self._data = np.empty((rows, cols), dtype='object')
            if cols == cols_sheet:
                # skip header
                curr_row = 1
                while curr_row <= rows and self._stop_trigger == 0:
                    for col in range(cols):
                        # check cell type:
                        self._check_format_xls(curr_row, col, worksheet, column_type)
                    curr_row += 1

                if self._errors == 0:
                    return self._data
                else:
                    self._has_errors = 1
            else:
                print dt.ERROR_COLUMNS.format(cols, self._sheet, cols_sheet)
                self._errors = 1
                self._has_errors = 1

    def _check_format_xls(self, pos, col, ws, column_type):
        cell_type = ws.cell_type(pos, col)
        if cell_type in column_type[col]:
            if cell_type == 2:
                # check integer:
                if dt.FIELDS_TYPES[self._sheet][col] == cell_type:
                    if self._isint(ws.cell_value(pos, col)) is False:
                        self._error_format_xls(pos, col, ws, 2)
                    else:
                        self._data[pos - 1, col] = ws.cell_value(pos, col)

            elif cell_type == 3:
                cell = ws.cell_value(pos, col)
                date_text = str(datetime.datetime(*xlrd.xldate_as_tuple(cell, self._workbook.datemode)))
                if self._isdate(date_text):
                    self._data[pos - 1, col] = date_text
            else:
                self._data[pos - 1, col] = ws.cell_value(pos, col)
        else:
            # curr_row + 1 to match with rows in Excel
            self._error_format_xls(pos, col, ws, dt.FIELDS_TYPES[self._sheet][col])

    def _error_format_xls(self, pos, col, ws, db_type):
        print dt.ERROR_VALIDATION.format(pos + 1, col + 1, ws.cell(pos, col).value, dt.DB_TYPES[db_type])

        self._errors += 1

        if self._stop is True:
            self._stop_trigger = 1
        pass

    @staticmethod
    def _isint(s):
        try:
            a = float(s)
            b = int(a)
        except ValueError:
            return False
        else:
            return a == b

    @staticmethod
    def _isfloat(s):
        try:
            float(s)
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def _isdate(s):
        for date_format in dt.DATE_FORMATS:
            try:
                datetime.datetime.strptime(s, date_format)
                return True
            except (ValueError, TypeError):
                pass
        return False

    @property
    def errors_count(self):
        # returns name of errors
        return self._errors

    @property
    def error(self):
        # Boolean Y | N
        return self._has_errors

    @property
    def data_shape(self):
        if self._type is "csv":
            return len(self._data.values()[0]), len(self._data)
        elif self._type is "xls":
            return self._data.shape


class DataTesting:
    """
    DataTesting is the tool to check if there will be errors during the process of uploading new data
    from CSV/Excel/Txt files. DataTesting is required to avoid blocking the database.
    """

    def __init__(self):
        pass


class DataToBD:
    """
    DataToBD uploads data from external sources into ERP_Database when has passed DataUpload and DataTesting.
    """

    def __init__(self):
        pass


class DBInMemory:
    """
    Create DB in memory to store persistent data (self._data.values())
    """

    def __init__(self):
        pass
