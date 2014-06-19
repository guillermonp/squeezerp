from PyQt4 import QtCore

from squeezerp.gui import ui_tools
from squeezerp.gui.dialogs.datatools_history.view import ViewDataToolsHistory


class ControllerDataToolsHistory(ViewDataToolsHistory):
    def __init__(self):
        ViewDataToolsHistory.__init__(self)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # connections and slots
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.connect(self.rbtn_by_errors, QtCore.SIGNAL("toggled(bool)"), self.view_group)
        self.connect(self.cbo_period, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.view_table)

        # import core functions to print as pdf file or export as xls or csv files
        #self.connect(self.export_action, QtCore.SIGNAL("triggered()"), )
        #self.connect(self.print_action, QtCore.SIGNAL("triggered()"), )

        self.worker_thread = ui_tools.WorkerThread()
