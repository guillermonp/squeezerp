from matplotlib.figure import Figure
from matplotlib import rc
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from squeezerp.modules.chart_options import chart_colors, chart_font


class PlotWidget(Canvas):
    def __init__(self, parent, x_dimension, y_dimension, x_label=None, y_label=None):
        super(PlotWidget, self).__init__(Figure())

        self.setParent(parent)
        self.figure = Figure((x_dimension, y_dimension))
        self.canvas = Canvas(self.figure)

        self.axes = self.figure.add_subplot(111)

        # navigation toolbar
        self.nav = NavigationToolbar(self.canvas, self)
        self.nav.hide()

        # background color = white
        self.figure.set_facecolor('white')

        self.plot_properties(x_label, y_label)
        self.plot_style()

    def plot_properties(self, x_label, y_label):

        if x_label and y_label is not None:
            self.axes.set_xlabel(x_label)
            self.axes.set_ylabel(y_label)

        self.figure.tight_layout()

    def plot_style(self):

        # change axes colors - grey
        axes = ["bottom", "top", "left", "right"]
        for ax in axes:
            self.axes.spines[ax].set_color(chart_colors["grey"])

        # change x-label and y-label color
        self.axes.xaxis.label.set_color(chart_colors["dark_grey"])
        self.axes.yaxis.label.set_color(chart_colors["dark_grey"])

        # change tick color
        self.axes.tick_params(axis='x', colors=chart_colors["grey"])
        self.axes.tick_params(axis='y', colors=chart_colors["grey"])

        # change font size - labels
        rc('font', **chart_font)

        # add grid - soft grey
        self.axes.grid(True)

    def plot(self):
        pass