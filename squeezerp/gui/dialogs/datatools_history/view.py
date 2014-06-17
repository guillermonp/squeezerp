from PyQt4 import QtCore
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QRadioButton

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QApplication


from squeezerp import resources
from squeezerp.modules.charts import PlotWidget
from squeezerp.gui import ui_strings

import sys


class ViewDataToolsHistory(QMainWindow):
    def __init__(self, parent=None):
        super(ViewDataToolsHistory, self).__init__(parent)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # DATATOOLS HISTORY WINDOWS:
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.setWindowTitle(ui_strings.DATATOOLS_HISTORY_TITLE)
        self._width = 700
        self._height = 380
        self._left_margin = 10
        self.resize(self._width, self._height)
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(self._width, self._height))
        self.setMaximumSize(QtCore.QSize(self._width, self._height))
        self.setWindowIcon(QIcon(resources.ICON_LOGO))

        # central widget
        self.central_widget = QWidget(self)

        # toolbar
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # add toolbar options
        self.export_action = QAction(QIcon(resources.ICON_EXPORT), 'Export (Ctrl+E)', self)
        self.export_action.setShortcut('Ctrl+E')

        self.print_action = QAction(QIcon(resources.ICON_PRINT), 'Print (Ctrl+P)', self)
        self.print_action.setShortcut('Ctrl+P')

        self.toolbar = self.addToolBar('Options')
        self.toolbar.addAction(self.export_action)
        self.toolbar.addAction(self.print_action)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # group input files
        self.group_period = QGroupBox(self.central_widget)
        self.group_period.setGeometry(QtCore.QRect(self._left_margin, 10, 250, 50))
        self.group_period.setTitle(ui_strings.DATATOOLS_HISTORY_FILTER)

        # group by:
        self.group_group_by = QGroupBox(self.central_widget)
        self.group_group_by.setGeometry(QtCore.QRect(270, 10, 420, 50))
        self.group_group_by.setTitle(ui_strings.DATATOOLS_HISTORY_GROUP)

        # group by: errors
        self.group_by_errors = QRadioButton(ui_strings.DATATOOLS_HISTORY_GROUP_ERROR, self.group_group_by)
        self.group_by_errors.setGeometry(QtCore.QRect(10, 10, 80, 50))

        # group by: status
        self.group_by_status = QRadioButton(ui_strings.DATATOOLS_HISTORY_GROUP_STATUS, self.group_group_by)
        self.group_by_status.setGeometry(QtCore.QRect(100, 10, 80, 50))

        # group by: no group
        self.group_by_no = QRadioButton(ui_strings.DATATOOLS_HISTORY_GROUP_NO, self.group_group_by)
        self.group_by_no.setGeometry(QtCore.QRect(190, 10, 80, 50))

        # combobox periods
        self.cbo_sheet = QComboBox(self.group_period)
        self.cbo_sheet.setGeometry(QtCore.QRect(self._left_margin, 20, 130, 20))

        # push button to update table
        self.btn_view = QPushButton(self.group_period)
        self.btn_view.setGeometry(QtCore.QRect(160, 20, 50, 20))
        self.btn_view.setText(ui_strings.DATATOOLS_HISTORY_VIEW)

        # table history
        self.tbl_errors = QTableWidget(self.central_widget)
        self.tbl_errors.setGeometry(QtCore.QRect(self._left_margin, 70, 680, 120))

        # chart
        self.plot_widget = PlotWidget(self.central_widget, 8, 2)
        self.plot_widget.setGeometry(QtCore.QRect(self._left_margin, 200, 680, 130))

        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    ui = ViewDataToolsHistory()
    ui.show()
    sys.exit(app.exec_())