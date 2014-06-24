import numpy as np

from matplotlib.figure import Figure
from matplotlib import rc
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from squeezerp.modules.chart_options import chart_colors, chart_font


class PlotWidget(Canvas):
    def __init__(self, parent, x_dimension, y_dimension):
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

        # global variables
        self.x_limit = None

        self.plot_style()

    def plot_properties(self, x_label, y_label, x_limit=None):
        """
        Plot properties and variables
            axis labels
            x axis label (limit)
        :param x_label: x axis labels
        :param y_label: y axis labels
        :param x_limit: number of x axis labels to display
        """

        if x_label and y_label is not None:
            self.axes.set_xlabel(x_label)
            self.axes.set_ylabel(y_label)

            self.x_limit = x_limit

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

    def plot_lines(self, x_values, y_values, *args):

        # number of columns - range
        columns = len(x_values)
        ind = np.arange(columns)

        # convert x_values to string and y_values to float - review!
        x_labels = np.array(x_values, dtype=str)
        y = np.array(y_values, dtype=float)

        # tick labels with dates
        if columns <= self.x_limit:
            self.axes.set_xticks(np.arange(columns))

        self.axes.xaxis.get_majorticklocs()
        self.axes.set_xticklabels(x_labels)

        # show y_values
        if not args:
            self.axes.plot(ind, y)
        else:
            # multiple series
            pass

        self.figure.tight_layout()

    def plot_bars(self):
        pass

    def plot_stats(self):
        pass

    def plot_pie(self):
        pass

    def plot_polar(self):
        pass