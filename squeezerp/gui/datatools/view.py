from PyQt4 import QtCore
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QProgressBar
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QFrame
from PyQt4.QtGui import QToolButton
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QRadioButton
from PyQt4.QtGui import QLineEdit

from squeezerp import resources
from squeezerp.gui import ui_strings

import sys
from PyQt4.QtGui import QApplication


class ViewDataTools(QMainWindow):
    def __init__(self, parent=None):
        super(ViewDataTools, self).__init__(parent)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # DATATOOLS WINDOWS:
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.setWindowTitle(ui_strings.DATATOOLS_TITLE)
        self._width = 680
        self._height = 560
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

        # DataTools description
        self.lbl_description = QLabel(self.central_widget)
        self.lbl_description.setGeometry(QtCore.QRect(0, 0, self._width, 30))
        self.lbl_description.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_description.setText(ui_strings.DATATOOLS_DESCRIPTION)

        # group input files
        self.group_input_file = QGroupBox(self.central_widget)
        self.group_input_file.setGeometry(QtCore.QRect(self._left_margin, 30, 660, 80))
        self.group_input_file.setTitle(ui_strings.DATATOOLS_GROUP_INPUT)

        # frame input files
        self.frame_inputs = QFrame(self.group_input_file)
        self.frame_inputs.setGeometry(QtCore.QRect(self._left_margin, 0, 270, 80))
        self.frame_inputs.setFrameShape(QFrame.StyledPanel)
        self.frame_inputs.setFrameShadow(QFrame.Raised)

        # label input type
        self.lbl_input_type = QLabel(self.frame_inputs)
        self.lbl_input_type.setGeometry(QtCore.QRect(20, 20, 60, 15))
        self.lbl_input_type.setText(ui_strings.DATATOOLS_INPUT_TYPE)

        # button xls
        self.btn_xls = QToolButton(self.frame_inputs)
        self.btn_xls.setGeometry(QtCore.QRect(20, 35, 35, 35))
        icon_xls = QIcon()
        icon_xls.addPixmap(QPixmap(resources.ICON_XLS), QIcon.Normal, QIcon.Off)
        self.btn_xls.setIcon(icon_xls)
        self.btn_xls.setIconSize(QtCore.QSize(24, 24))
        self.btn_xls.setCheckable(True)
        self.btn_xls.setAutoExclusive(True)
        self.btn_xls.setObjectName("xls_button")

        # button csv
        self.btn_csv = QToolButton(self.frame_inputs)
        self.btn_csv.setGeometry(QtCore.QRect(60, 35, 35, 35))
        icon_csv = QIcon()
        icon_csv.addPixmap(QPixmap(resources.ICON_CSV), QIcon.Normal, QIcon.Off)
        self.btn_csv.setIcon(icon_csv)
        self.btn_csv.setIconSize(QtCore.QSize(24, 24))
        self.btn_csv.setCheckable(True)
        self.btn_csv.setAutoExclusive(True)
        self.btn_csv.setObjectName("csv_button")

        # checkbox csv with headers
        self.chk_csv_headers = QCheckBox(ui_strings.DATATOOLS_WITH_HEADERS, self.frame_inputs)
        self.chk_csv_headers.setGeometry(QtCore.QRect(100, 45, 110, 15))
        self.chk_csv_headers.setEnabled(False)

        # TextEdit + PushButton (FindFolder)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # lbl sheet name
        self.lbl_file_path = QLabel(self.group_input_file)
        self.lbl_file_path.setGeometry(QtCore.QRect(250, 20, 120, 15))
        self.lbl_file_path.setText(ui_strings.DATATOOLS_SELECT_FILE)

        self.txt_file = QLineEdit(self.group_input_file)
        self.txt_file.setGeometry(QtCore.QRect(250, 35, 160, 20))
        self.txt_file.setReadOnly(True)

        self.btn_path = QPushButton(self.group_input_file)
        self.btn_path.setGeometry(QtCore.QRect(410, 34, 50, 22))
        self.btn_path.setText(ui_strings.DATATOOLS_SELECT_BUTTON)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # lbl sheet name
        self.lbl_sheet_name = QLabel(self.group_input_file)
        self.lbl_sheet_name.setGeometry(QtCore.QRect(500, 20, 120, 15))
        self.lbl_sheet_name.setText(ui_strings.DATATOOLS_SHEET_NAME)

        # Combobox select sheet - initially does not contain values
        self.cbo_sheet = QComboBox(self.group_input_file)
        self.cbo_sheet.setGeometry(QtCore.QRect(500, 35, 130, 20))

        # data grid to visualize error messages
        self.tbl_errors = QTableWidget(self.central_widget)
        self.tbl_errors.setGeometry(QtCore.QRect(self._left_margin, 420, 660, 100))

        # data grid to visualize those records with errors.
        self.tbl_uploaded_data = QTableWidget(self.central_widget)
        self.tbl_uploaded_data.setGeometry(QtCore.QRect(self._left_margin, 120, 500, 220))

        # group run options
        self.group_run_options = QGroupBox(self.central_widget)
        self.group_run_options.setGeometry(QtCore.QRect(520, 120, 150, 220))
        self.group_run_options.setTitle(ui_strings.DATATOOLS_GROUP_RUN)

        # Errors summary:
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # group summary errors
        self.group_errors = QGroupBox(self.central_widget)
        self.group_errors.setGeometry(QtCore.QRect(self._left_margin, 350, 660, 60))
        self.group_errors.setTitle(ui_strings.DATATOOLS_HEADER_ERRORS)

        # lbl records
        self.lbl_records = QLabel(self.group_errors)
        self.lbl_records.setGeometry(QtCore.QRect(165, 15, 80, 15))
        self.lbl_records.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_records.setText(ui_strings.DATATOOLS_RECORDS)

        self.txt_records = QLineEdit(self.group_errors)
        self.txt_records.setGeometry(QtCore.QRect(165, 30, 80, 20))
        self.txt_records.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_records.setReadOnly(True)

        # lbl errors
        self.lbl_errors = QLabel(self.group_errors)
        self.lbl_errors.setGeometry(QtCore.QRect(275, 15, 80, 15))
        self.lbl_errors.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_errors.setText(ui_strings.DATATOOLS_ERRORS)

        self.txt_errors = QLineEdit(self.group_errors)
        self.txt_errors.setGeometry(QtCore.QRect(275, 30, 80, 20))
        self.txt_errors.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_errors.setReadOnly(True)

        # lbl time
        self.lbl_time = QLabel(self.group_errors)
        self.lbl_time.setGeometry(QtCore.QRect(385, 15, 80, 15))
        self.lbl_time.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_time.setText(ui_strings.DATATOOLS_TIME)

        self.txt_time = QLineEdit(self.group_errors)
        self.txt_time.setGeometry(QtCore.QRect(385, 30, 80, 20))
        self.txt_time.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_time.setReadOnly(True)

        # history button
        self.btn_history = QToolButton(self.group_errors)
        self.btn_history.setGeometry(QtCore.QRect(500, 25, 100, 25))
        icon_history = QIcon()
        icon_history.addPixmap(QPixmap(resources.ICON_HISTORY), QIcon.Normal, QIcon.Off)
        self.btn_history.setIcon(icon_history)
        self.btn_history.setIconSize(QtCore.QSize(20, 20))
        self.btn_history.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btn_history.setText(ui_strings.DATATOOLS_HISTORY)
        self.btn_history.setCheckable(True)
        self.btn_history.setAutoExclusive(True)
        self.btn_history.setObjectName("history_button")
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # btn data uploader
        self.btn_data_uploader = QPushButton(ui_strings.DATATOOLS_DATA_UPLOADER, self.group_run_options)
        self.btn_data_uploader.setGeometry(QtCore.QRect(10, 120, 90, 25))
        self.btn_data_uploader.setCheckable(True)
        self.btn_data_uploader.setAutoExclusive(True)
        self.btn_data_uploader.setFlat(False)

        # btn data testing
        self.btn_data_testing = QPushButton(ui_strings.DATATOOLS_DATA_TESTING, self.group_run_options)
        self.btn_data_testing.setEnabled(False)
        self.btn_data_testing.setGeometry(QtCore.QRect(10, 150, 90, 25))
        self.btn_data_testing.setCheckable(True)
        self.btn_data_testing.setAutoExclusive(True)

        # btn data to database
        self.btn_data_db = QPushButton(ui_strings.DATATOOLS_DATA_DB, self.group_run_options)
        self.btn_data_db.setEnabled(False)
        self.btn_data_db.setGeometry(QtCore.QRect(10, 179, 91, 23))
        self.btn_data_db.setCheckable(True)
        self.btn_data_db.setAutoExclusive(True)

        # frame run options
        self.frame_run = QFrame(self.group_run_options)
        self.frame_run.setGeometry(QtCore.QRect(10, 30, 130, 80))
        self.frame_run.setFrameShape(QFrame.StyledPanel)
        self.frame_run.setFrameShadow(QFrame.Raised)

        # option process until first error
        self.rbtn_process_error = QRadioButton(ui_strings.DATATOOLS_PROCESS_ERROR, self.frame_run)
        self.rbtn_process_error.setGeometry(QtCore.QRect(0, 0, 150, 20))

        # option process all data
        self.rbtn_process_all = QRadioButton(ui_strings.DATATOOLS_PROCESS_ALL, self.frame_run)
        self.rbtn_process_all.setGeometry(QtCore.QRect(0, 20, 150, 30))

        # checkbox to filter by records with errors.
        #self.chk_filter_errors = QCheckBox(ui_strings.DATATOOLS_FILTER_ERRORS, self.frame_run)
        #self.chk_filter_errors.setGeometry(QtCore.QRect(0, 50, 100, 15))
        #self.chk_filter_errors.setEnabled(False)

        # icons -> pass - error: Initially are empty labels
        # if not started -> ICON_MINI_WAIT
        # if error -> ICON_DELETE
        # if pass -> ICON_CHECK

        # state icon data uploader
        self.lbl_state_du = QLabel(self.group_run_options)
        self.lbl_state_du.setGeometry(QtCore.QRect(110, 120, 20, 20))
        self.lbl_state_du.setPixmap(QPixmap(resources.ICON_MINI_WAIT))
        self.lbl_state_du.setScaledContents(True)

        # state icon data to database
        self.lbl_state_dt = QLabel(self.group_run_options)
        self.lbl_state_dt.setGeometry(QtCore.QRect(110, 150, 20, 20))
        self.lbl_state_dt.setPixmap(QPixmap(resources.ICON_MINI_WAIT))
        self.lbl_state_dt.setScaledContents(True)

         # state icon data testing
        self.lbl_state_db = QLabel(self.group_run_options)
        self.lbl_state_db.setGeometry(QtCore.QRect(110, 180, 20, 20))
        self.lbl_state_db.setPixmap(QPixmap(resources.ICON_MINI_WAIT))
        self.lbl_state_db.setScaledContents(True)

        # progress bar
        self.progress_bar = QProgressBar(self.central_widget)
        self.progress_bar.setGeometry(QtCore.QRect(self._left_margin, 530, 660, 15))
        self.progress_bar.setMaximum(100)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setOrientation(QtCore.Qt.Horizontal)
        self.progress_bar.setInvertedAppearance(False)
        self.progress_bar.setTextDirection(QProgressBar.TopToBottom)

        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ui = ViewDataTools()
    ui.show()
    sys.exit(app.exec_())