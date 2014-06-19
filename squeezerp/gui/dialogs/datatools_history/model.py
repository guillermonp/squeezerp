import sys
from PyQt4.QtGui import QApplication

from squeezerp.database import database_core as dbcore, database_queries as db_q
from squeezerp.gui import ui_tools
from squeezerp.gui.dialogs.datatools_history.controller import ControllerDataToolsHistory
from squeezerp.gui.dialogs.datatools_history import app_data


class ModelDataToolsHistory(ControllerDataToolsHistory):
    def __init__(self):
        ControllerDataToolsHistory.__init__(self)

        # DataUploaderHistory variables
        self.db = dbcore.DatabaseOperations()

        # initialize with period = 1 week
        self.period = 1
        self.query = db_q.select_datauploader_history
        self.snippet_query = db_q.snippet_du_history_period_1week

        # add combobox periods
        ui_tools.load_combobox(self.cbo_period, app_data.PERIODS.values())

        # show initial data

        self.view_table()

    def view_table(self):
        """ visualize table DataUploaderHistory """

        headers, data = dbcore.DatabaseOperations().sql_fetch_data(self.query, self.snippet_query)
        ui_tools.view_table(self.tbl_uploads, headers, data)

    def view_group(self):
        """
        visualize table DataUploaderHistory group by:
            day - errors: Number of uploads with errors per day.
            day - status: Uploading status type per day.
            no group: show all data.
        """
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = ModelDataToolsHistory()
    ui.show()
    sys.exit(app.exec_())