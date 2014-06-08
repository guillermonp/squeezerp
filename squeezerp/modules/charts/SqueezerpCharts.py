from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar


from PyQt4.QtGui import QDialog
from PyQt4.Qt import QMenu


class PlotWidget(Canvas):
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(Figure())

        self.setParent(parent)
        self.figure = Figure()
        self.canvas = Canvas(self.figure)

        # navigation toolbar
        self.nav = NavigationToolbar(self.canvas, self)
        self.nav.hide()

        # background color = white
        self.figure.patch.set_facecolor('white')

        self.add_plot('x label', 'y label', 'title')

    def add_plot(self, x_label, y_label, title):

        ax = self.figure.add_subplot(111)
        self.figure.tight_layout()

    def style(self):
        pass

    def plot(self):
        pass


class PlotTools(QDialog, PlotWidget):
    def __init__(self):
        super(PlotTools, self).__init__(self)
        self.chart_tools = self.nav

    def options(self):
        chart_menu = QMenu()
        chart_tools = chart_menu.addAction("chart tools")
        chart_tools_home = chart_tools.addAction("home")
        chart_tools_zoom = chart_tools.addAction("zoom")
        chart_tools_pan = chart_tools.addAction("padding")
        chart_tools_save = chart_tools.addAction("save")

        chart_type = chart_menu.addAction("chart type")
        chart_type_line = chart_type.addAction("chart line")
        chart_type_column = chart_type.addAction("chart column")

        action = chart_menu.exec_(self.mapToGlobal(pos))

        if action == chart_tools_home:
            pass

    def chart_home(self):
        self.chart_tools.home()

    def chart_zoom(self):
        self.chart_tools.zoom()

    def chart_pan(self):
        self.chart_tools.pan()

    def chart_save(self):
        self.chart_tools.save_figure()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    ui = PlotTools()
    ui.show()
    sys.exit(app.exec_())