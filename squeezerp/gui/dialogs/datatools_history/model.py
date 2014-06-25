import sys
import numpy as np

from PyQt4 import QtCore
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
        self.query = None
        self.snippet = None

        # add combobox periods - set combobox = 1 week
        ui_tools.load_combobox(self.cbo_period, app_data.PERIODS.values(), sort=False)

        # initialize with period = 1 week
        self.period = 1

        _index = self.cbo_period.findText(app_data.PERIODS[self.period])
        self.cbo_period.setCurrentIndex(_index)

        # controller part (exceptionally MV) - to avoid double queries
        self.connect(self.cbo_period, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.view_table)

        # show initial data
        self.view_table()

    def view_table(self):
        """ visualize table DataUploaderHistory """
        period_name = str(self.cbo_period.currentText())
        self.period = [k for k, v in app_data.PERIODS.iteritems() if v == period_name][0]

        self.query = db_q.select_datauploader_history
        self.period_filter()
        headers, data = self.db.sql_fetch_data(self.query, self.snippet)
        ui_tools.view_table(self.tbl_uploads, headers, data)

        if self.rbtn_by_errors.isChecked():
            self.rbtn_by_errors.setChecked(False)

        # display chart
        self.plot()

    def view_group(self):
        """
        visualize table DataUploaderHistory group by:
            day - errors: Number of uploads with errors per day.
            day - status: Uploading status type per day.
            no group: show all data.
        """
        if self.rbtn_by_errors.isChecked():
            self.query = db_q.select_datauploader_history_errors

        headers, data = self.db.sql_fetch_data(self.query)
        ui_tools.view_table(self.tbl_uploads, headers, data)

        self.plot_group_info()

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

    def plot(self):
        """
        update gui with the corresponding chart - PlotWidget

        data comes from custom queries.
            days - SUM(#errors)
        """
        x_lbl = "days"
        y_lbl = "# errors"
        chart_query = db_q.select_datauploader_history_daily_errors
        chart_snippet = db_q.snippet_du_history_day_order

        # just data, no headers
        if self.period != 4:
            chart_data = np.asarray(self.db.sql_fetch_data(chart_query, [self.snippet, chart_snippet])[1])
        else:
            chart_data = np.asarray(self.db.sql_fetch_data(chart_query, chart_snippet)[1])

        if len(chart_data) > 0:
            days = chart_data[:, 0]
            errors = chart_data[:, 1]
            self.plot_widget.plot_properties(x_label=x_lbl, y_label=y_lbl, x_limit=7)
            self.plot_widget.plot_lines(x_values=days, y_values=errors)

    def plot_group_info(self):
        """
        update gui with the corresponding chart - PlotWidget

        plotted data:
            x_label: day
            y_label: two series - uploads and uploads with errors

            this chart includes legend! - not implemented
        """
        x_lbl = "days"
        y_lbl = "records"
        chart_query = self.query

        chart_data = np.asarray(self.db.sql_fetch_data(chart_query)[1])
        print chart_data

        if len(chart_data) > 0:
            days = chart_data[:, 0]
            uploads = chart_data[:, 1]
            errors = chart_data[:, 2]
            self.plot_widget.plot_properties(x_label=x_lbl, y_label=y_lbl, x_limit=7)
            self.plot_widget.plot_lines(days, uploads, errors)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = ModelDataToolsHistory()
    ui.show()
    sys.exit(app.exec_())