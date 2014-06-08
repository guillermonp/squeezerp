from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar


class PlotWidget(Canvas):
    def __init__(self, parent):
        super(PlotWidget, self).__init__(Figure())

        self.setParent(parent)
        self.figure = Figure((7.0, 2.0))
        self.canvas = Canvas(self.figure)

        self.axes = self.figure.add_subplot(111)

        # navigation toolbar
        self.nav = NavigationToolbar(self.canvas, self)
        self.nav.hide()

        # background color = white
        self.figure.set_facecolor('white')

        self.plot_properties()
        self.plot_style()

    def plot_properties(self):

        self.axes.set_ylabel('test')
        self.axes.set_xlabel('test')
        self.figure.tight_layout()

    def plot_style(self):
        self.axes.spines['bottom'].set_color('grey')