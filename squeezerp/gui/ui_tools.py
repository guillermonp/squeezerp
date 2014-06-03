"""
Qt Tools:
    --WorkerThread
    --UploadErrors
    --load_table
"""

import time

from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtCore import Qt


class WorkerThread(QThread):
    def __init__(self):
        super(WorkerThread, self).__init__()

    def run(self):
        time.sleep(3)


def load_data(table, headers, data):
        _columns = len(headers)
        table.setColumnCount(_columns)
        remove_rows(table)

        for rw, row in enumerate(data):
            table.insertRow(rw)
            for index, colItem in enumerate(row):
                item = QTableWidgetItem(str(colItem))
                table.setItem(rw, index, item)
                item.setData(Qt.UserRole, row)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        # table options
        load_table_options(table, headers)

        # auto fit
        auto_fit_table(table)


def load_data_csv(table, headers, data):
    _columns = len(headers)
    table.setColumnCount(_columns)
    remove_rows(table)

    for rw in range(len(data[0])):
        table.insertRow(rw)
        for c in range(len(data)):
            item = QTableWidgetItem(str(data[c][rw]))
            table.setItem(rw, c, item)
            item.setData(Qt.UserRole, rw)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        # table options
        load_table_options(table, headers)

        # auto fit
        auto_fit_table(table)


def remove_rows(table):
    for i in range(table.rowCount()):
            table.removeRow(0)


def remove_headers(table):
    table.horizontalHeader().setVisible(False)


def auto_fit_table(table):
    table.setVisible(False)
    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    table.setVisible(True)


def load_table_options(table, headers):
    table.horizontalHeader().setVisible(True)
    table.setHorizontalHeaderLabels(headers)
    table.horizontalHeader().setStretchLastSection(True)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setSortingEnabled(False)