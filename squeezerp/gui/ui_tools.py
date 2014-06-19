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


class MyTableWidgetItem(QTableWidgetItem):
    def __init__(self, text, sort_key):
        QTableWidgetItem.__init__(self, text, QTableWidgetItem.UserType)
        self.sort_key = sort_key

    def __lt__(self, other):
        return self.sort_key < other.sort_key


def load_datatools(table, headers, data):
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


def load_datatools_csv(table, headers, data):
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


def view_table(table, headers, data):
    _columns = len(headers)
    table.setColumnCount(_columns)
    remove_rows(table)

    for rw, row in enumerate(data):
        table.insertRow(rw)
        for index, colItem in enumerate(row):
            item = MyTableWidgetItem(str(colItem), colItem)
            item.setData(Qt.UserRole, rw)
            table.setItem(rw, index, item)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    # initially: ascending order on column 0 (id)
    table.sortItems(0, Qt.AscendingOrder)

    # table options
    view_table_options(table, headers)

    # auto fit
    auto_fit_table(table)


def view_table_options(table, headers):
    table.horizontalHeader().setVisible(True)
    table.setHorizontalHeaderLabels(headers)
    table.horizontalHeader().setStretchLastSection(True)

    # remove row numbers: avoid confusion with possible id's
    table.verticalHeader().setVisible(False)

    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setSortingEnabled(True)


def load_combobox(combobox, options):
    """ load combobox options - ordered ascending """
    sheets = sorted(options)

    for sheet in sheets:
        combobox.addItem(sheet)