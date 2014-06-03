import os
import sys
import csv
import datetime
import time
from collections import OrderedDict

import xlrd
import numpy as np
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QFileDialog

from squeezerp import resources
from squeezerp.core import tools
from squeezerp.database.database_core import DatabaseOperations
from squeezerp.gui import ui_styles, ui_tools, ui_strings
from squeezerp.gui.datatools import app_data
from squeezerp.gui.datatools.controller import ControllerDataTools


class ModelDataTools(ControllerDataTools):
    def __init__(self):
        ControllerDataTools.__init__(self)

        # -- global variables
        self._path = None
        self._headers = None
        self._sheet = None
        self._stop = None
        self._type = None

        # -- DataUploader variables
        self._data = None
        self._workbook = None
        self._stop_trigger = None

        # -- DataUploader - DataTesting variables
        self._errors = None
        self._has_errors = None
        self.uploaded_errors = None
        self._error_type = None

        self.add_combobox_values()

    def add_combobox_values(self):
        """ Import available sheets to be uploaded """
        _sheets = sorted(app_data.SHEETS.keys())
        for sheet in _sheets:
            self.cbo_sheet.addItem(sheet)

    def csv_headers(self):
        self._headers = True

    def csv_option(self):
        self._type = "csv"
        self.chk_csv_headers.setEnabled(True)

    def xls_option(self):
        self._type = "xls"
        self.chk_csv_headers.setEnabled(False)

    def run_error(self):
        self._stop = True
        #self.chk_filter_errors.setEnabled(False)

    def run_all(self):
        self._stop = False
        #self.chk_filter_errors.setEnabled(True)

    def update_progress(self, value, total):
        self.progress_bar.setValue(float(value) / total * 100)

    @staticmethod
    def state_button(state, *args):
        for btn in args:
            btn.setEnabled(state)

    @staticmethod
    def clean_textbox(*args):
        for txt in args:
            txt.setText("")

    @QtCore.pyqtSlot()
    def file_dialog(self):

        if self.btn_csv.isChecked():
            file_name = QFileDialog.getOpenFileName(self, 'Select input file', "C:/", "(*.csv)")
            self.txt_file.setText(file_name)
        elif self.btn_xls.isChecked():
            file_name = QFileDialog.getOpenFileName(self, 'Select input file', "C:/", "(*.xls)")
            self.txt_file.setText(file_name)
        else:
            self.show_error_message("input_error")

    @staticmethod
    def show_state(label, state):
        if state == "pause":
            label.setPixmap(QPixmap(resources.ICON_MINI_WAIT))
        if state == "error":
            label.setPixmap(QPixmap(resources.ICON_ERROR))
        if state == "pass":
            return label.setPixmap(QPixmap(resources.ICON_PASS))

    def show_error_message(self, error_type):
        error_message = QMessageBox(self)
        error_message.setWindowTitle(ui_strings.DATATOOLS_MESSAGE_ERROR)
        msg = ""
        if error_type == "run_error":
            msg = ui_strings.DATATOOLS_SELECT_RUN_OPTION
            error_message.setDetailedText(app_data.ERROR_RUN_OPTION)
        elif error_type == "input_error":
            msg = ui_strings.DATATOOLS_SELECT_INPUT_TYPE
            error_message.setDetailedText(app_data.ERROR_INPUT_OPTION)
        elif error_type == "file_error":
            msg = ui_strings.DATATOOLS_SELECT_INPUT_TYPE
            error_message.setDetailedText(app_data.ERROR_FILE_OPTION)

        error_message.detailedText()
        error_message.setText(msg)
        error_message.exec_()

    @QtCore.pyqtSlot()
    def datauploader(self):
        # start thread
        self.worker_thread.start()

        # inputs
        self._sheet = str(self.cbo_sheet.currentText())
        self._data = None
        self._workbook = None
        self._errors = 0
        self._has_errors = 0
        self._stop_trigger = 0
        self.tbl_errors.setStyleSheet("")
        self.uploaded_errors = UploadErrors()

        # state
        self.clean_textbox(self.txt_records, self.txt_errors, self.txt_time)
        self.show_state(label=self.lbl_state_du, state="pause")
        self.progress_bar.setValue(0)
        self.state_button(False, self.btn_data_testing, self.btn_data_db)
        self._error_type = "success"

        # tables
        ui_tools.remove_headers(self.tbl_errors)
        ui_tools.remove_headers(self.tbl_uploaded_data)
        ui_tools.remove_rows(self.tbl_errors)
        ui_tools.remove_rows(self.tbl_uploaded_data)

        start = time.time()

        # path
        if self.txt_file.text() == "":
            self.show_error_message("file_error")
            return 1
        else:
            path, f_extension = os.path.splitext(str(self.txt_file.text()))
            self._path = str(self.txt_file.text())
            # check file extension
            if not ((self.btn_csv.isChecked() and f_extension == ".csv") or (
                    self.btn_xls.isChecked() and f_extension == ".xls")):
                self.show_error_message("file_error")
                return 1

        if self._stop is not None:
            if self._type == "csv":
                delimiter = ","
                if self._headers is True:
                    data = self.import_csv(delimiter=delimiter, hd_option=True)
                else:
                    data = self.import_csv(delimiter=delimiter, hd_option=False)
            elif self._type == "xls":
                data = self.import_excel
            else:
                self.show_error_message("input_error")
                return 1
        else:
            self.show_error_message("run_error")
            return 1

        finish = time.time()

        # results:
        if self.error == 1:  # errors
            self.tbl_errors.setStyleSheet(ui_styles.DATATOOLS_ERROR_TABLE)
            self.show_state(label=self.lbl_state_du, state="error")
            ui_tools.load_data(self.tbl_errors, app_data.HEADER_ERROR, self.uploaded_errors.table)
        else:
            self.tbl_errors.setStyleSheet(ui_styles.DATATOOLS_PASS_TABLE)
            self.show_state(label=self.lbl_state_du, state="pass")
            # enable Data Testing
            self.state_button(True, self.btn_data_testing)

        # records and errors
        self.txt_records.setText(str(self.data_shape[0]))
        self.txt_errors.setText(str(self.errors_count))
        self.txt_time.setText(str(round((finish - start), 3)))

        # new entry in DataUploaderHistory
        self.add_history(start, finish)

        # print results
        if data is not None and self._type == "csv":
            ui_tools.load_data_csv(self.tbl_uploaded_data, app_data.TABLE_HEADERS[self._sheet], data)
        elif data is not None and self._type == "xls":
            ui_tools.load_data(self.tbl_uploaded_data, app_data.TABLE_HEADERS[self._sheet], data)

    def import_csv(self, delimiter, hd_option=None):
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
            self._errors = 1
            self._error_type = "csv"
            self.uploaded_errors.add_error("error", "", "", app_data.ERROR_READ_CSV_MSG, "",
                                           app_data.ERROR_READ_CSV_CORRECT)

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
        if app_data.SHEETS[sheet] == num_cols:
            column_types = app_data.FIELDS_TYPES[sheet]
            for col in range(num_cols):
                self.update_progress(col, num_cols - 1)
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
            self.uploaded_errors.add_error("error", "", "",
                                           app_data.ERROR_COLUMNS_MSG.format(num_cols, sheet, app_data.SHEETS[sheet]),
                                           "", "")
            return 1

    def _error_format_csv(self, col, pos, cell, cell_format):
        cell_format = app_data.DB_TYPES[cell_format]
        self._error_type = "input"
        self.uploaded_errors.add_error("error", pos + 1, col + 1, app_data.ERROR_VAL_MSG,
                                       app_data.ERROR_VAL_VALUE.format(cell),
                                       app_data.ERROR_VAL_CORRECT.format(cell_format))
        self._errors += 1
        if self._stop is True:
            return 1

    @property
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
        sheet = self._sheet
        if sheet in app_data.SHEETS:
            worksheet = self._workbook.sheet_by_name(sheet)
            column_type = app_data.FIELDS_TYPES_XLS[sheet]
            cols = worksheet.ncols
            cols_sheet = app_data.SHEETS[sheet]
            # exclude column header
            rows = worksheet.nrows - 1
            # empty array [None] to store data. dtype must be an object due to the array doesn't have an unique type
            records = rows
            self._data = np.empty((rows, cols), dtype='object')
            if cols == cols_sheet:
                # skip header
                curr_row = 1
                while curr_row <= rows and self._stop_trigger == 0:
                    # update progress bar
                    self.update_progress(curr_row, records)
                    for col in range(cols):
                        # check cell type:
                        self._check_format_xls(curr_row, col, worksheet, column_type)
                    curr_row += 1

                if self._errors == 0:
                    return self._data
                else:
                    self._has_errors = 1
            else:
                self.uploaded_errors.add_error("error", "", "",
                                               app_data.ERROR_COLUMNS_MSG.format(cols, sheet, app_data.SHEETS[sheet]),
                                               "", "")
                self._error_type = "xls"
                self.progress_bar.setValue(100)
                self._errors = 1
                self._has_errors = 1

    def _check_format_xls(self, pos, col, ws, column_type):
        cell_type = ws.cell_type(pos, col)
        if cell_type in column_type[col]:
            if cell_type == 2:
                # check integer:
                if app_data.FIELDS_TYPES[self._sheet][col] == cell_type:
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
            self._error_format_xls(pos, col, ws, app_data.FIELDS_TYPES[self._sheet][col])

    def _error_format_xls(self, pos, col, ws, db_type):
        self._error_type = "input"
        self.uploaded_errors.add_error("error", pos + 1, col + 1, app_data.ERROR_VAL_MSG,
                                       app_data.ERROR_VAL_VALUE.format(ws.cell(pos, col).value),
                                       app_data.ERROR_VAL_CORRECT.format(app_data.DB_TYPES[db_type]))
        self._errors += 1
        if self._stop is True:
            self._stop_trigger = 1

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
        for date_format in app_data.DATE_FORMATS:
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

    def add_history(self, start, end):
        _sheet_name = self._sheet
        _file_name = self._path
        _file_size = tools.get_file_size(_file_name)
        _format = self._type
        _has_error = self._has_errors
        _records = self.data_shape[0]
        _errors = self._errors
        _error_type = app_data.ERROR_TYPES[self._error_type]
        _start = start
        _end = end

        fields = (_sheet_name, _file_name, _file_size, _format, _has_error, _records, _errors, _error_type, _start, _end)
        DatabaseOperations().insert_history_uploader(fields)


class UploadErrors:
    def __init__(self):
        self.errors = []

    def add_error(self, err_type, rw, cl, msg, err_value, err_correct):
        _type = err_type
        _row = str(rw)
        _column = str(cl)
        _message = msg
        _err_value = str(err_value)
        _correct = err_correct

        error = [_type, _row, _column, _message, _err_value, _correct]
        self.errors.append(error)

    @property
    def table(self):
        return self.errors


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = ModelDataTools()
    ui.show()
    sys.exit(app.exec_())