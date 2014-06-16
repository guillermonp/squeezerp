from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from squeezerp.modules.chart_options import chart_colors

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

        self.plot_properties()
        self.plot_style()

    def plot_properties(self):

        self.axes.set_ylabel('test')
        self.axes.set_xlabel('test')
        self.figure.tight_layout()

    def plot_style(self):

        # change axes colors - grey
        axes = ["bottom", "top", "left", "right"]
        for ax in axes:
            self.axes.spines[ax].set_color(chart_colors["grey"][0])

        # change x-label and y-label color
        self.axes.xaxis.label.set_color(chart_colors["dark_grey"][0])
        self.axes.yaxis.label.set_color(chart_colors["dark_grey"][0])

        # change tick color
        self.axes.tick_params(axis='x', colors=chart_colors["grey"][0])
        self.axes.tick_params(axis='y', colors=chart_colors["grey"][0])

        # change font size

        # add grid - soft grey
        self.axes.grid(True)