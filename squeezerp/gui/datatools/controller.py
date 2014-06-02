from PyQt4 import QtCore

from squeezerp.gui.datatools.view import ViewDataTools
from squeezerp.tools import ui_tools


class ControllerDataTools(ViewDataTools):

    def __init__(self):
        ViewDataTools.__init__(self)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # connections and slots
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.connect(self.btn_data_uploader, QtCore.SIGNAL("clicked()"), self.datauploader)
        self.connect(self.btn_csv, QtCore.SIGNAL("clicked()"), self.csv_option)
        self.connect(self.chk_csv_headers, QtCore.SIGNAL("clicked()"), self.csv_headers)
        self.connect(self.btn_xls, QtCore.SIGNAL("clicked()"), self.xls_option)
        self.connect(self.rbtn_process_error, QtCore.SIGNAL("clicked()"), self.run_error)
        self.connect(self.rbtn_process_all, QtCore.SIGNAL("clicked()"), self.run_all)
        self.connect(self.btn_path, QtCore.SIGNAL("clicked()"), self.file_dialog)

        self.worker_thread = ui_tools.WorkerThread()