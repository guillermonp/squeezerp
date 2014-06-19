import sys
from PyQt4.QtGui import QApplication

from squeezerp.database import database_core as db_core
from squeezerp.database import database_queries as db_q
from squeezerp.gui import ui_tools

from squeezerp.gui.dialogs.datatools_history import app_data
from squeezerp.gui.dialogs.datatools_history.controller import ControllerDataToolsHistory


class ModelDataToolsHistory(ControllerDataToolsHistory):
    def __init__(self):
        ControllerDataToolsHistory.__init__(self)

        # DataUploaderHistory variables
        self.db = db_core.DatabaseOperations()
        self.query = db_q.select_datauploader_history

        # initialize with period = 1 week
        self.period = 1
        self.snippet = db_q.snippet_du_history_period_1week

        # add combobox periods - set combobox = 1 week
        ui_tools.load_combobox(self.cbo_period, app_data.PERIODS.values())
        _index = self.cbo_period.findText(app_data.PERIODS[self.period])
        self.cbo_period.setCurrentIndex(_index)

        # show initial data
        self.view_table()

    def view_table(self):
        """ visualize table DataUploaderHistory """
        period_name = str(self.cbo_period.currentText())
        self.period = [k for k, v in app_data.PERIODS.iteritems() if v == period_name][0]

        self.period_filter()
        headers, data = self.db.sql_fetch_data(self.query, self.snippet)

        ui_tools.view_table(self.tbl_uploads, headers, data)

    def view_group(self):
        """
        visualize table DataUploaderHistory group by:
            day - errors: Number of uploads with errors per day.
            day - status: Uploading status type per day.
            no group: show all data.
        """
        pass

    def period_filter(self):
        if self.period == 0:
            self.snippet = db_q.snippet_du_history_period_today
        elif self.period == 1:
            self.snippet = db_q.snippet_du_history_period_1week
        elif self.period == 2:
            self.snippet = db_q.snippet_du_history_period_1month
        elif self.period == 3:
            self.snippet = db_q.snippet_du_history_period_3month
        else:
            self.snippet = None  # no snippets

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = ModelDataToolsHistory()
    ui.show()
    sys.exit(app.exec_())