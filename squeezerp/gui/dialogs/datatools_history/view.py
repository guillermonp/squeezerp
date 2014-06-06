from PyQt4 import QtCore
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QWidget

from squeezerp import resources
from squeezerp.gui import ui_strings

import sys
from PyQt4.QtGui import QApplication


class ViewDataToolsHistory(QMainWindow):
    def __init__(self, parent=None):
        super(ViewDataToolsHistory, self).__init__(parent)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # DATATOOLS HISTORY WINDOWS:
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.setWindowTitle(ui_strings.DATATOOLS_HISTORY_TITLE)
        self._width = 500
        self._height = 300
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

        #


if __name__ == "__main__":

    app = QApplication(sys.argv)
    ui = ViewDataToolsHistory()
    ui.show()
    sys.exit(app.exec_())